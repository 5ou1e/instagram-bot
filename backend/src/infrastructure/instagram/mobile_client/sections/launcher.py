from yarl import URL

from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.generators import generate_uuid_v4_hex
from src.infrastructure.instagram.common.utils import (
    build_signed_body,
    dumps_orjson,
    instagram_app_user_agent_from_android_device_info,
)
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class LauncherSection:

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

    async def mobile_config(self):
        uri = constants.LAUNCHER_MOBILE_CONFIG_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "com.bloks.www.caa.login.login_homepage",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
                "x-ig-nav-chain": "SelfFragment:self_profile:2:main_profile:1755687768.793:::1755687768.793,ProfileMediaTabFragment:self_profile:3:button:1755687769.244:::1755687769.244,ProfileMediaTabFragment:self_profile:4:button:1755687771.634:::1755687771.634,SettingsScreenFragment:main_settings_screen:5:button:1755687771.916:::1755687771.916,com.bloks.www.caa.login.aymh_single_profile_screen_entry:com.bloks.www.caa.login.aymh_single_profile_screen_entry:6:button:1755687779.67:::1755687779.67,IgCdsScreenNavigationLoggerModule:com.bloks.www.caa.login.login_homepage:7:button:1755687780.534:::1755687780.534,com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:8:button:1755687783.171:::1755687783.171",
                "x-fb-rmd": "state=URL_ELIGIBLE",
            }
        )

        data = {
            "bool_opt_policy": "0",
            "mobileconfig": "",
            "api_version": "10",
            "client_context": dumps_orjson(["opt,value_hash"]),
            "unit_type": "2",
            "use_case": "STANDARD",
            "query_hash": "afbf25f577b10c6784e55995f46fac65b39623739edd37210e7b39e830c28026",
            "ts": "1755687768",
            "_uid": str(self._local_data.user_id),
            "device_id": self._local_data.device_id,
            "_uuid": self._local_data.device_id,
            "fetch_mode": "CONFIG_SYNC_ONLY",
            "fetch_type": "ASYNC_FULL",
            "request_data_query_hash": "afbf25f577b10c6784e55995f46fac65b39623739edd37210e7b39e830c28026",
        }

        signed_data = build_signed_body(dumps_orjson(data))

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=signed_data,
        )

        response = await self._request_handler(request)

        return response

    async def rmd(self):
        uri = "rmd/"
        url = URL(constants.BASE_INSTAGRAM_URL) / uri

        user_agent = instagram_app_user_agent_from_android_device_info(
            self._device_info,
            self._version_info,
        )

        headers = headers = {
            "priority": "u=3, i",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "rmd-mapfetcher",
            "x-fb-privacy-context": "4760009080727693",
            "x-fb-request-analytics-tags": dumps_orjson(
                {
                    "network_tags": {
                        "product": self._version_info.app_id,
                        "retry_attempt": "0",
                    },
                    "application_tags": "rmd",
                }
            ),
            "x-fb-server-cluster": "True",
            "x-ig-app-id": self._version_info.app_id,
            "x-ig-capabilities": "3brTv10=",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": user_agent,
            "x-fb-conn-uuid-client": generate_uuid_v4_hex(),
            "x-fb-http-engine": "MNS/TCP",
            "x-fb-rmd": "state=URL_ELIGIBLE",
        }

        params = {
            "access_token": self._version_info.access_token,
            "rule_context": "instagram_prod",
            "net_iface": "Unknown",
            "reason": "SESSION_CHANGE",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response

    async def banyan_banyan(self):
        uri = "banyan/banyan/"
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
            "is_private_share": "false",
            "views": dumps_orjson(
                [
                    "direct_user_search_keypressed",
                    "direct_user_search_nullstate",
                    "direct_inbox_active_now",
                    "call_recipients",
                ]
            ),
            "IBCShareSheetParams": dumps_orjson({"size": 5}),
            "is_real_time": "false",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response
