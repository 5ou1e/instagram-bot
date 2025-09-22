from uuid import uuid4

from yarl import URL

from src.domain.shared.interfaces.instagram.exceptions import (
    InstagramError,
    NotFoundError,
    UserIdNotFound,
)
from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.utils import build_signed_body, dumps_orjson
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class UserSection:

    def __init__(
        self,
        state: MobileInstagramClientState,
        request_handler: RequestHandler,
        logger: Logger,
    ):
        self._state = state
        self._request_handler = request_handler
        self.logger = logger

        self._device_info = self._state.device_info
        self._local_data = self._state.local_data
        self._version_info = self._state.version_info

    async def follow_user(self, user_id: str) -> bool:
        """Подписка на пользователя по user_id"""

        uri = constants.FRIENDSHIPS_CREATE_URI.format(user_id=user_id)
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "following",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
                "Priority": "u=3",
                "X-Fb-Rmd": "state=URL_ELIGIBLE",
            }
        )

        data = {
            "user_id": str(user_id),
            "include_follow_friction_check": "1",
            "radio_type": "wifi-none",  # ?????? если mobile - непонятно какое значение
            "_uid": self._local_data.user_id,
            "device_id": self._local_data.android_id,
            "_uuid": self._local_data.device_id,
            # "nav_chain": "MainFeedFragment:feed_timeline:1:cold_start:1753513599.349:10#230#301:3684454714105803249,UserDetailFragment:profile:12:media_owner:1753517807.682::,ProfileMediaTabFragment:profile:13:button:1753517808.672::,FollowListFragment:following:14:button:1753517814.772::",
            # "container_module": "following",
            # "follow_ranking_token": "4aeaf5017f394bcab074ec8c7ac9a6e2|{ig_session_data.user_id}|osr"
        }

        signed_data = build_signed_body(dumps_orjson(data))

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=signed_data,
        )

        try:
            response = await self._request_handler(request)
        except NotFoundError as e:
            raise UserIdNotFound(user_id=user_id) from e
        if response.get("status") == "ok":
            return True
        else:
            raise InstagramError(message=str(response))

    async def get_user_followers_by_user_id(self, user_id: str, max_id: int) -> list:

        rank_token = uuid4()

        uri = constants.FRIENDSHIPS_USER_FOLLOWERS_URI.format(user_id=user_id)
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        params = {
            "rank_token": str(rank_token),
            "max_id": str(max_id),
            # "count": 25, # max is 25
        }

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "X-Ig-Client-Endpoint": "unknown",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
                "Priority": "u=3",
                "X-Fb-Rmd": "state=URL_ELIGIBLE",
            }
        )

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        if response.get("status") == "ok":
            users = response.get("users", [])
            return users
        else:
            raise InstagramError(message=str(response))

    async def get_user_info_by_id(self, user_id: str):

        uri = constants.USERS_USER_INFO_URI.format(user_id=user_id)
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
        )

        response = await self._request_handler(request)
        return response

    async def get_limited_interactions_reminder(self):

        uri = constants.USERS_GET_LIMITED_INTERACTIONS_REMINDER_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "X-Ig-Client-Endpoint": "com.bloks.www.caa.login.login_homepage",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
                "x-ig-nav-chain": "SelfFragment:self_profile:2:main_profile:1755687768.793:::1755687768.793,ProfileMediaTabFragment:self_profile:3:button:1755687769.244:::1755687769.244,ProfileMediaTabFragment:self_profile:4:button:1755687771.634:::1755687771.634,SettingsScreenFragment:main_settings_screen:5:button:1755687771.916:::1755687771.916,com.bloks.www.caa.login.aymh_single_profile_screen_entry:com.bloks.www.caa.login.aymh_single_profile_screen_entry:6:button:1755687779.67:::1755687779.67,IgCdsScreenNavigationLoggerModule:com.bloks.www.caa.login.login_homepage:7:button:1755687780.534:::1755687780.534,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:8:button:1755687783.171:::1755687783.171,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:9:button:1755691660.675:::1755691660.675",
            }
        )

        signed_data = build_signed_body(dumps_orjson({}))

        params = {"signed_body": signed_data}

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response
