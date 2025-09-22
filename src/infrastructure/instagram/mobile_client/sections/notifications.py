from yarl import URL

from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class NotificationsSection:

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

    async def get_notification_settings(self):
        uri = constants.NOTIFICATIONS_GET_NOTIFICATION_SETTINGS_URI
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
                "x-ig-nav-chain": "SelfFragment:self_profile:2:main_profile:1755687768.793:::1755687768.793,ProfileMediaTabFragment:self_profile:3:button:1755687769.244:::1755687769.244,ProfileMediaTabFragment:self_profile:4:button:1755687771.634:::1755687771.634,SettingsScreenFragment:main_settings_screen:5:button:1755687771.916:::1755687771.916,com.bloks.www.caa.login.aymh_single_profile_screen_entry:com.bloks.www.caa.login.aymh_single_profile_screen_entry:6:button:1755687779.67:::1755687779.67,IgCdsScreenNavigationLoggerModule:com.bloks.www.caa.login.login_homepage:7:button:1755687780.534:::1755687780.534,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:8:button:1755687783.171:::1755687783.171",
                "x-fb-rmd": "state=URL_ELIGIBLE",
            }
        )

        params = {
            "content_type": "post_and_comments",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response

    async def badge(self):
        uri = constants.NOTIFICATIONS_BADGE_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "com.bloks.www.caa.login.login_homepage",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
                "x-fb-rmd": "state=URL_ELIGIBLE",
                "x-ig-salt-ids": "220140399,332020310,974466465,974460658",
            }
        )

        data = {
            "phone_id": self._local_data.family_device_id,
            "trigger": "NOTIFICATION_FEED_HEART_ICON",
            "user_ids": self._local_data.user_id,
            "device_id": self._local_data.device_id,
            "_uuid": self._local_data.device_id,
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        response = await self._request_handler(request)

        return response
