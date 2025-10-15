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
    BadResponseError,
    ChallengeRequired,
    NetworkError,
)
from src.domain.shared.interfaces.instagram.web_client.config import (
    WebInstagramClientConfig,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.user_agent.entities import UserAgent
from src.infrastructure.instagram.common.password_encrypter import PasswordEncrypter


class InstagramWebAPI:
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

    def get_cookies(self) -> dict:
        return {cookie.key: cookie.value for cookie in self._session.cookie_jar}

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
            "Request: \nURL: %s \nHeaders: %s, \nCookies: %s, \nData: %s \nProxy: %s",
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
                "Неизвестная ошибка Web-api клиента: %s %s ", type(e), e
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

        return json_data

    async def post_account_recovery_send_ajax(self, username: str) -> dict:
        return await self.send_request(
            "POST",
            "https://www.instagram.com/accounts/account_recovery_send_ajax/",
            data={"email_or_username": username, "recaptcha_challenge_field": ""},
            headers={
                "x-requested-with": "XMLHttpRequest",
                "x-csrftoken": self.csrftoken,
                "Connection": "Keep-Alive",
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "en-US",
                "User-Agent": self._user_agent,
                "Cookies": self._cookies_string,
            },
        )

    async def login_ajax(
        self,
        username: str,
        password: str,
        relogin: bool = False,
        parse_user: bool = False,
    ) -> dict:
        encrypter = PasswordEncrypter()
        enc_password = encrypter.encrypt_v0(password)

        data = {
            "username": username,
            "enc_password": enc_password,
            "queryParams": {},
            "optIntoOneTap": "false",
        }

        return await self.send_request(
            "POST",
            "https://www.instagram.com/accounts/login/ajax/",
            data=data,
            headers={
                "x-requested-with": "XMLHttpRequest",
                "x-csrftoken": self.csrftoken,
                "Connection": "Keep-Alive",
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "en-US",
                "User-Agent": self._user_agent,
                "Cookies": self._cookies_string,
            },
        )

    async def accounts_edit(self) -> dict:

        return await self.send_request(
            "GET",
            "https://www.instagram.com/api/v1/accounts/edit/web_form_data/",
            headers={
                "x-requested-with": "XMLHttpRequest",
                "x-csrftoken": self.csrftoken,
                "Connection": "Keep-Alive",
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "en-US",
                "User-Agent": self._user_agent,
                "Cookies": self._cookies_string,
            },
        )

    async def friendships_follow(self, user_id: str) -> dict:
        return await self.send_request(
            "POST",
            f"https://www.instagram.com/web/friendships/{user_id}/follow/",
            data={},
            headers={
                "x-requested-with": "XMLHttpRequest",
                "x-csrftoken": self.csrftoken,
                "Connection": "Keep-Alive",
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "en-US",
                "User-Agent": self._user_agent,
                "Cookies": self._cookies_string,
            },
        )
