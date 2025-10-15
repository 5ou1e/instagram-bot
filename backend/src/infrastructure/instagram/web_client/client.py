import aiohttp
from aiograpi import Client as AiograpiClient
from aiograpi.utils import gen_token
from yarl import URL

from src.domain.aggregates.proxy.entities import Proxy
from src.domain.shared.exceptions23 import (
    AuthorizationError,
    BadPassword,
    ChallengeRequired,
    ChallengeType,
    EmailNotMatchedError,
    InstagramError,
    ResetLinkNotSentError,
    ResetPasswordError,
    ResetPasswordLinkExpiredError,
    UnauthorizedError,
    UserNotFoundError,
)
from src.domain.shared.interfaces.instagram.web_client.client import WebInstagramClient
from src.domain.shared.interfaces.instagram.web_client.config import (
    WebInstagramClientConfig,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.user_agent.entities import UserAgent
from src.infrastructure.instagram.common.password_encrypter import PasswordEncrypter
from src.infrastructure.instagram.mobile_client.utils.extractors import (
    extract_challenge_path,
    extract_encrypted_ap_context_from_challenge_path,
)
from src.infrastructure.instagram.web_client.apis.graphql_api.api import (
    InstagramGraphQL,
)
from src.infrastructure.instagram.web_client.apis.wep_api.api import InstagramWebAPI
from src.infrastructure.instagram.web_client.utils.extractors import (
    extract_masked_email,
    extract_payload_data_from_reset_password_url,
    parse_password_reset_recovery_success_client,
)
from src.infrastructure.instagram.web_client.utils.other import match_masked_email


class WebInstagramClientImpl(WebInstagramClient):
    """Клиeнт Instagram"""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        web_api: InstagramWebAPI,
        graphql_api: InstagramGraphQL,
        aiograpi: AiograpiClient,
        params: WebInstagramClientConfig,
        logger: Logger,
    ):
        self._session = session
        self._graphql = graphql_api
        self._web_api = web_api
        self._aiograpi = aiograpi
        self._proxies = {}
        self.set_proxy(params.proxy)
        self.logger = logger

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._session.close()

    def set_proxy(self, proxy: Proxy) -> None:
        if not proxy:
            return
        proxy_url = proxy.url
        self._graphql.set_proxy(proxy)
        self._web_api.set_proxy(proxy)
        self._proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }

    def set_user_agent(self, user_agent: UserAgent) -> None:
        user_agent_string = user_agent.string
        self._web_api.set_user_agent(user_agent)
        self._graphql.set_user_agent(user_agent)

    def set_user_agent_mobile(self, user_agent: UserAgent) -> None:
        self._web_api.set_user_agent_mobile(user_agent)
        self._graphql.set_user_agent_mobile(user_agent)

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

    async def request_reset_password(self, username: str, email: str) -> None:
        res = await self._web_api.post_account_recovery_send_ajax(username)

        message = res.get("message", "Неизвестная ошибка")
        if "email sent" not in res.get("title", "").lower():
            if "no users found" in str(message).lower():
                raise UserNotFoundError(
                    username=username,
                    message=message,
                )

            raise ResetLinkNotSentError(
                message=message,
            )

        masked_email = extract_masked_email(res["body"])

        if not match_masked_email(masked_email, email):
            raise EmailNotMatchedError(
                masked_email=masked_email,
                email=email,
            )

    async def change_password_by_link(
        self,
        password: str,
        reset_password_url: str,
    ) -> bool:

        encrypter = PasswordEncrypter()
        hashed_password = encrypter.encrypt_v0(password)

        params = extract_payload_data_from_reset_password_url(reset_password_url)
        json_data = await self._graphql.post_password_reset_submit_action_handler(
            hashed_password, params
        )

        if parse_password_reset_recovery_success_client(json_data):
            return True

        if len(self.get_cookies().get("sessionid", "")) >= 20:
            await self.logger.info(
                "Инстаграм установил sessionid, считаем, что пароль изменен"
            )
            # Если инста в этот момент установла сессию, считаем что пароль изменен
            return True

        if challenge_path := extract_challenge_path(json_data):
            raise ChallengeRequired(
                type=ChallengeType.AUTH_PLATFORM_CODE_ENTRY,
                challenge_path=challenge_path,
                message=f"Чекпоинт подтверждения почты: {challenge_path}",
            )
        if (
            "expired token. please request a new password reset link"
            in str(json_data).lower()
        ):
            raise ResetPasswordLinkExpiredError(message=str(json_data))

        raise ResetPasswordError(message=f"{json_data}")

    async def send_verification_code_for_auth_platform_challenge(
        self,
        code: str,
        challenge_path: str,
    ):
        encrypted_ap_context = extract_encrypted_ap_context_from_challenge_path(
            challenge_path
        )
        await self._graphql.use_auth_platform_code_mutation(code, encrypted_ap_context)

    async def like_media(self, media_id: str):
        return True

    async def authorize_by_login_and_password(
        self,
        username: str,
        password: str,
    ) -> None:
        # Response: {"user": true, "authenticated": false, "status": "ok"}
        response = await self._web_api.login_ajax(username, password)
        await self.logger.error(response)
        if not response.get("authenticated", False):
            if response.get("user", False):
                raise BadPassword(password=password, message=str(response))
            else:
                raise UserNotFoundError(username=username, message=str(response))

        if not response.get("status", False) == "ok":
            raise AuthorizationError(message=str(response))

    async def authorize_by_sessionid(self, sessionid: str):
        self.set_cookies(
            {
                "sessionid": sessionid,
            }
        )

        res = await self._web_api.accounts_edit()

        authorized = self.get_cookies().get("sessionid", None)
        if not authorized:
            raise UnauthorizedError(message=str(res))

    async def follow_user(self, user_id: str) -> None:
        user_id = str(user_id)

        result = await self._web_api.friendships_follow(user_id)
        if not result.get("status") == "ok":
            raise InstagramError(message=str(result))
