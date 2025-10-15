import asyncio
import json
from json import JSONDecodeError

import aiohttp
from aiograpi import Client as AiograpiClient
from aiohttp import ClientResponse
from instagrapi.utils import gen_token
from yarl import URL

from src.domain.aggregates.proxy.entities import Proxy
from src.domain.shared.exceptions23 import (
    BadRequestError,
    BadResponseError,
    ChallengeRequired,
    InstagramError,
    NetworkError,
)
from src.domain.shared.interfaces.instagram.web_client.config import (
    WebInstagramClientConfig,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.user_agent.entities import UserAgent
from src.infrastructure.instagram.common.generators import current_timestamp
from src.infrastructure.instagram.web_client.types import ParamsFromResetPassUrl


class InstagramGraphQL:
    app_id = "936619743392459"

    def __init__(
        self,
        session: aiohttp.ClientSession,
        params: WebInstagramClientConfig,
        logger: Logger,
        max_retries_on_network_errors: int = 0,
        delay_before_retries_on_network_errors: int = 0,
    ):
        self._max_retries_on_network_errors = max_retries_on_network_errors
        self._delay_before_retries_on_network_errors = (
            delay_before_retries_on_network_errors
        )
        self.logger = logger
        self._session = session
        self._aiograpi = AiograpiClient()
        self._proxies = {}
        self._user_agent = None
        self._user_agent_mobile = None
        self.set_proxy(params.proxy)
        self.set_user_agent(params.user_agent)
        self.set_user_agent_mobile(params.user_agent_mobile)
        self.set_cookies(params.cookies)

    def set_user_agent(self, user_agent: UserAgent) -> None:
        self._user_agent = (
            user_agent.string
            if user_agent
            else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        )

    def set_user_agent_mobile(self, user_agent: UserAgent) -> None:
        self._user_agent_mobile = (
            user_agent.string
            if user_agent
            else "Instagram 167.0.0.24.120 Android (26/8.0.0; 480dpi; 1080x1776; Sony; F8331; F8331; qcom; ru_RU; 256966583)"
        )

    def set_proxy(self, proxy: Proxy | None = None) -> None:
        if proxy:
            proxy_url = proxy.url
            self._proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }
        else:
            self._proxies = {}

    def get_cookies(self) -> dict:
        return {cookie.key: cookie.value for cookie in self._session.cookie_jar}

    def set_cookies(self, cookies: dict) -> None:
        """Устанавливает новые куки полностью"""
        if cookies is None:
            cookies = {}
        # Если в cookies нет 'csrftoken', генерим новый
        if "csrftoken" not in cookies:
            cookies["csrftoken"] = gen_token(64)

        for name, value in cookies.items():
            self._session.cookie_jar.update_cookies(
                {name: value},
                response_url=URL("https://www.instagram.com"),
            )

    @property
    def _cookies_string(self) -> str:
        cookies = {cookie.key: cookie.value for cookie in self._session.cookie_jar}
        return ";".join(f"{k}={v}" for k, v in cookies.items())

    @property
    def csrftoken(self) -> str:
        for cookie in self._session.cookie_jar:
            if cookie.key.lower() == "csrftoken":
                return cookie.value
        return gen_token(64)

    async def send_request(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ):
        await self.logger.debug(
            "Request parameters: \nURL: %s \nHeaders: %s, \nCookies: %s, \nData: %s \nProxy: %s",
            url,
            headers,
            {cookie.key: cookie.value for cookie in self._session.cookie_jar},
            data,
            self._proxies["http"],
        )
        try:
            async with self._session.request(
                method,
                url,
                data=data,
                headers=headers,
                proxy=self._proxies.get("https", None),
            ) as resp:
                await self.log_response_data(resp)

        except aiohttp.ClientError as e:
            raise NetworkError(message=f"{e}") from e
        except asyncio.TimeoutError as e:
            raise NetworkError(message=f"Timeout error") from e
        except Exception as e:
            await self.logger.error(
                "Неизвестная ошибка GrahpQL клиента: %s %s ", type(e), e
            )
            raise e

        return await self.parse_insta_response(resp)

    async def log_response_data(self, resp: ClientResponse):
        text = await resp.text()
        cookies = {cookie.key: cookie.value for cookie in self._session.cookie_jar}

        await self.logger.debug(
            "Response:\nStatus: %s\nResponse: %s\nCookies: %s",
            resp.status,
            text,
            cookies,
        )

    async def parse_insta_response(self, resp: ClientResponse) -> dict:
        text = await resp.text()
        prefix = "for (;;);"
        if text.startswith(prefix):
            text = text[len(prefix) :]

        try:
            json_data = json.loads(text)
        except JSONDecodeError as e:
            raise BadResponseError(
                message=f"Ошибка парсинга JSON, response: {text[:200]}"
            )

        message = json_data.get("message", "")
        if "checkpoint_required" in message:
            challenge_path = json_data.get("checkpoint_url")
            raise ChallengeRequired(type=None, challenge_path=challenge_path)

        if "error" in json_data and "errorDescription" in json_data:
            if (
                "there was a problem with this request"
                in str(json_data["errorDescription"]).lower()
            ):
                raise BadRequestError(message=f"Некорректный запрос: {json_data}")
            raise InstagramError(message=f"{json_data}")

        return json_data

    async def post_password_reset_submit_action_handler(
        self,
        hashed_password: str,
        params: ParamsFromResetPassUrl,
    ) -> dict:

        return await self.send_request(
            "POST",
            "https://www.instagram.com/api/v1/bloks/apps/com.instagram.account_security.password_reset_submit_action_handler/",
            data={
                "enc_new_password1": hashed_password,
                "enc_new_password2": hashed_password,
                "uidb36": params["uidb36"],
                "token": params["token"],
                "error_state": '{"state_id":2030432425,"index":0,"type_name":"str"}',
                "source": params["source"],
                "is_caa": params["is_caa"],
                "afv": params["afv"],
                "cni": "null",
                "nest_data_manifest": "true",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": self._user_agent,
                "Cookie": self._cookies_string,
                "X-CSRFToken": self.csrftoken,
                "X-IG-App-ID": self.app_id,  # Instagram Web ID
            },
        )

    async def use_auth_platform_code_mutation(
        self,
        code: str,
        encrypted_ap_context: str,
    ):
        """Запрос для подтверждения восстановления пароля кодом с почты
        !!!Что важно, это не работает с ОБЫЧНЫМ ЮЗЕР-АГЕНТОМ!!!
        """

        url = "https://www.instagram.com/api/graphql"

        data = {
            "av": "0",
            "__d": "www",
            "__user": "0",
            "__a": "1",
            "__req": "1a",  # mb different
            "__hs": "20252.HYP:instagram_web_pkg.2.1...0",
            "dpr": "1",
            "__ccg": "MODERATE",  # mb MODERATE
            "__rev": "1023811211",
            "__s": "8ms71s:4cvxoy:a3s2p1",
            "__hsi": "7515508275692613681",  # mb random
            "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU29zEdEc8co2qwJw5ux609vCwjE1EE2Cw8G1Dz81s8hwGxu786a3a1YwBgao6C0Mo2swaOfK0EUjwGzEaE2iwNwmE2eUlwhE2Lw6OyES1TwVwDwHg2ZwrUdUbGweG269wr86C1mgcEed6goK10xKi2K7E5y1rwcObBKu9w4UwFw",  # mb random
            "__csr": "gq_i24h4HQyagGPAOaVbnqjCiGqBKdUDQjmcHhpLKiqbypul0CzUoyui8uagkg89QifyHDUO9D8HAoCibG4999Br8leVoCRz8nBx6fwGx6iiQUKq2KVqxy4-6UyEKiXKjgjUK8zE9Ux0DwhK5K00lKGlU3JppQ951q1swPwnE2BxEg1mK5U5afg2jCm0iZ03GUbo0gZw3H20aq0LC3ufwrA3t03sSmt0dBwbBolwaupm00AK80Na032O",  # mb random
            "__comet_req": "7",
            "lsd": "AVqSPmOzKLg",  # mb random
            "jazoest": "2991",  # mb random
            "__spin_r": "1023811211",
            "__spin_b": "trunk",
            "__spin_t": current_timestamp(),
            "__crn": "comet.igweb.PolarisAuthPlatformCodeEntryRoute",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAuthPlatformSubmitCodeMutation",
            "variables": json.dumps(
                {
                    "input": {
                        "client_mutation_id": "1",
                        "actor_id": "0",
                        "code": code,
                        "encrypted_ap_context": encrypted_ap_context,
                    }
                }
            ),
            "server_timestamps": "true",
            "doc_id": "24471258032464286",
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": self._user_agent_mobile,
            "Cookie": self._cookies_string,
            "X-CSRFToken": self.csrftoken,
            "X-IG-App-ID": self.app_id,  # Instagram Web ID
            "X-Asbd-Id": "359341",
            "X-Fb-Friendly-Name": "useAuthPlatformSubmitCodeMutation",
            "X-Fb-Lsd": "AVqSPmOzKLg",
        }

        return await self.send_request(
            "POST",
            url,
            data=data,
            headers=headers,
        )
