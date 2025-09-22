import gzip
from urllib.parse import urlencode

from yarl import URL

from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.generators import (
    current_timestamp_ms,
    generate_uuid_v4_string,
)
from src.infrastructure.instagram.common.utils import dumps_orjson
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class FeedSection:

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

    async def get_feed_timeline_i_api(self) -> dict:
        """Подписка на пользователя по user_id"""
        uri = constants.FEED_TIMELINE_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "Content-Encoding": "gzip",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "feed_timeline",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=0",
                "x-cm-bandwidth-kbps": "1876.105",
                "x-cm-latency": "3.666",
                "x-fb": "1",
                "x-ads-opt-out": "0",
                "x-ig-transfer-encoding": "chunked",
            }
        )

        current_timestamp = current_timestamp_ms()
        session_id = generate_uuid_v4_string()

        data = {
            "has_camera_permission": "0",
            "feed_view_info": dumps_orjson(
                [
                    {
                        "media_id": "3703054020150160348_61713625421",
                        "version": 24,
                        "media_pct": 0.8782353,
                        "time_info": {"10": 686, "25": 686, "50": 686, "75": 686},
                        "was_share_tapped": False,
                        "client_position": 0,
                        "author_id": "61713625421",
                        "product_type": "clips",
                        "media_type": "2",
                    }
                ]
            ),
            "organic_realtime_information": dumps_orjson(
                [
                    {
                        "item_id": "3703054020150160348",
                        "item_type": 1,
                        "session_id": session_id,
                        "container_module": "feed_timeline",
                        "multi_ads_type": 0,
                        "seen_states": [
                            {
                                "media_id": "3703054020150160348_61713625421",
                                "media_time_spent": [-1],
                                "impression_timestamp": current_timestamp - 150,
                                "media_percent_visible": -1.0,
                            }
                        ],
                    }
                ]
            ),
            "phone_id": self._local_data.family_device_id,
            "max_id": "KCEAZaQ2_7UYYzN1VSJ2cfZjMxaOKDcMFwAA3Osh_wLkYzMWtLLA35hmRgIYEGNvbGRfc3RhcnRfZmV0Y2hCMiiJAgACvrFq8VNfMw12ROqWEWQzDmSjWu8-UTMQzEvvMUZhM5AbSmw86mEzEBXFvZ7oYDMWjig3DBcAAJe0SjmCdWIzGuzNJVquXzOeW8j91iKgMim-hjLI918zr3sGm7cSZDOxaYA_wZtOMzRDh2YItgMztQo0KWGLYzM1wzIk4PNjM7QzowoICVUzuMsi9Ck9UTPBdCFy68lgM8KWxBLmA2QzxAcy9iGKYDPNGT3_w9RjM1Mxyc-Ep2Iz29KlACoCZDPc6yH_AuRjM96vIHsZl1Qz3mc6XKUMYzNkRTzJ_RNiM2WkNv-1GGMz5CfKDPjyXzPwyL7dA-tjM3VVInZx9mMze9wzZxR2WjNW7viqig0A",
            "client_view_state_media_list": dumps_orjson(
                [
                    {"id": "3703054020150160348_61713625421", "type": 0},
                    {"id": "25341232451094", "type": 161},
                    {"id": "3703074285802378613_61713625421", "type": 49},
                    {"id": "3702830488578597989_195284417", "type": 0},
                ]
            ),
            "reason": "pagination",
            "battery_level": "24",
            "timezone_offset": "10800",
            "client_recorded_request_time_ms": current_timestamp,
            "device_id": self._local_data.device_id,
            "request_id": generate_uuid_v4_string(),
            "is_pull_to_refresh": "0",
            "_uuid": self._local_data.device_id,
            "push_disabled": "true",
            "is_charging": "1",
            "is_dark_mode": "0",
            "will_sound_on": "0",
            "session_id": session_id,
            "bloks_versioning_id": self._version_info.bloks_version_id,
        }

        encoded = urlencode(data).encode("utf-8")
        compressed = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=compressed,
        )

        response = await self._request_handler(request)

        return response

    async def get_feed_timeline_b_api(self) -> dict:

        uri = constants.FEED_TIMELINE_URI
        url = URL(constants.INSTAGRAM_API_B_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "Content-Encoding": "gzip",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "feed_timeline",
                "X-Fb-Friendly-Name": f"IgApi: {uri}_tail",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=0",
                "x-cm-bandwidth-kbps": "1876.105",
                "x-cm-latency": "3.666",
                "x-fb": "1",
                "x-ads-opt-out": "0",
                "x-ig-transfer-encoding": "chunked",
            }
        )

        data = {
            "has_camera_permission": "0",
            "feed_view_info": "[]",
            "phone_id": self._local_data.family_device_id,
            "reason": "cold_start_fetch",
            "battery_level": "24",
            "timezone_offset": "10800",
            "client_recorded_request_time_ms": current_timestamp_ms(),
            "device_id": self._local_data.device_id,
            "request_id": generate_uuid_v4_string(),
            "is_pull_to_refresh": "0",
            "_uuid": self._local_data.device_id,
            "push_disabled": "true",
            "is_charging": "1",
            "is_dark_mode": "0",
            "will_sound_on": "0",
            "session_id": generate_uuid_v4_string(),
            "bloks_versioning_id": self._version_info.bloks_version_id,
        }

        encoded = urlencode(data).encode("utf-8")
        compressed = gzip.compress(encoded)

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=compressed,
        )

        response = await self._request_handler(request)

        return response

    async def get_reels_tray(self) -> dict:
        uri = constants.FEED_REELS_TRAY_URI
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
                "Priority": "u=0",
                "X-Ig-Transfer-Encoding": "chunked",
                "X-Fb-Rmd": "state=URL_ELIGIBLE",
            }
        )

        data = {
            "reason": "cold_start",
            "timezone_offset": "10800",
            "tray_session_id": generate_uuid_v4_string(),
            "request_id": generate_uuid_v4_string(),
            "_uuid": self._local_data.device_id,
            "page_size": "50",
        }

        request = HttpRequest(
            method="POST",
            url=url,
            headers=headers,
            data=data,
        )

        response = await self._request_handler(request)

        return response
