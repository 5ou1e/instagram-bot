from yarl import URL

from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.generators import generate_uuid_v4_string
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class DirectSection:

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

    async def direct_v2_get_precence(self) -> dict:

        uri = constants.DIRECT_V2_GET_PRESENCE_URI
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
            }
        )

        params = {
            "suggested_followers_limit": "100",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response

    async def direct_v2_get_pending_requests_preview(self):
        uri = constants.DIRECT_V2_GET_PENDING_REQUESTS_PREVIEW_URI
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
            }
        )

        params = {
            "pending_inbox_filters": [],
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response

    async def direct_v2_inbox(self):
        uri = constants.DIRECT_V2_INBOX_URI
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
            }
        )

        params = {
            "visual_message_return_type": "unseen",
            "igd_request_log_tracking_id": generate_uuid_v4_string(),
            "no_pending_badge": "true",
            "thread_message_limit": 5,
            "persistentBadging": "true",
            "limit": 15,
            "is_prefetching": "false",
            "fetch_reason": "initial_snapshot",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response

    async def direct_v2_get_presence_active_now(self):
        uri = constants.DIRECT_V2_GET_PRESENCE_ACTIVE_NOW_URI
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
            }
        )

        params = {
            "recent_thread_limit": 0,
            "suggested_followers_limit": 100,
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response
