from typing import Dict

from src.domain.shared.interfaces.instagram.mobile_client.entities.android_device_info import (
    MobileClientAndroidDeviceInfo,
)
from src.domain.shared.interfaces.instagram.mobile_client.entities.local_data import (
    MobileInstagramClientLocalData,
)
from src.infrastructure.instagram.common.generators import (
    device_languages_from_device_locale,
    generate_uuid_v4_hex,
    pigeon_rawclienttime,
    utc_timezone_offset,
)
from src.infrastructure.instagram.common.utils import (
    instagram_app_user_agent_from_android_device_info,
)
from src.infrastructure.instagram.mobile_client.instagram_version_info import (
    InstagramAppVersionInfo,
)


class MobileInstagramClientHeadersFactory:
    """Фабрика заголовков для Instagram API"""

    @classmethod
    def api_headers(
        cls,
        device_info: MobileClientAndroidDeviceInfo,
        version_info: InstagramAppVersionInfo,
        local_data: MobileInstagramClientLocalData,
    ) -> Dict[str, str]:
        """Базовые заголовки API v1 запросов"""

        accept_language = f"{device_info.locale.replace('_', '-')}, en-US"
        device_locale = f"{device_info.locale.replace('-', '_')}"

        bandwidth_metrics = local_data.bandwith_metrics

        headers = {
            # "content-length": 0,  # Aiohttp - автоматически
            "Accept-Encoding": "zstd",
            "Accept-Language": accept_language,
            "X-Ig-App-Locale": device_locale,
            "X-Ig-Mapped-Locale": device_locale,
            "X-Ig-Device-Locale": device_locale,
            "X-Ig-App-Id": version_info.app_id,
            "X-Ig-Capabilities": version_info.capabilities,
            "X-Ig-Connection-Type": device_info.connection_type,
            # fb
            "X-Fb-Client-Ip": "True",
            "X-Fb-Server-Cluster": "True",
            "X-Fb-Connection-Type": device_info.connection_type,
            "X-Fb-Http-Engine": "MNS/TCP",  # TODO "MNS/TCP" Возможно тут Liger или это от версии прилы зависит
            "X-Tigon-Is-Retry": "False",
            "X-Fb-Conn-Uuid-Client": generate_uuid_v4_hex(),
            # UUID соединения ( в оригинале не меняется на каждый запрос )
            "X-Ig-Device-Id": local_data.device_id,
            "X-Pigeon-Session-Id": local_data.pigeon_session_id,
            "X-Ig-Bandwidth-Speed-Kbps": f'{bandwidth_metrics["bandwidth_speed_kbps"]:.3f}',
            "X-Ig-Bandwidth-Totalbytes-B": str(
                bandwidth_metrics["bandwidth_totalbytes_b"]
            ),
            "X-Ig-Bandwidth-Totaltime-Ms": str(
                bandwidth_metrics["bandwidth_totaltime_ms"]
            ),
            "X-Ig-Android-Id": local_data.android_id,
            "X-Pigeon-Rawclienttime": pigeon_rawclienttime(),
            "X-Ig-Family-Device-Id": local_data.family_device_id,
            "X-Ig-Device-Languages": device_languages_from_device_locale(
                device_info.locale
            ),
            "X-Ig-Timezone-Offset": str(utc_timezone_offset(device_info.timezone)),
            # "x-fb-request-analytics-tags": dumps_orjson(
            #     {
            #         "network_tags": {
            #             "product": "567067343352427",
            #             "purpose": "fetch",
            #             "surface": "undefined",
            #             "request_category": "api",
            #             "retry_attempt": "0",
            #         }
            #     }
            # ),
            # "x-ig-salt-ids": "",  # 34/58 (58.5%) '220140399,332020310,974466465,974460658'
        }

        if local_data.user_id:
            headers["Ig-U-Ds-User-Id"] = local_data.user_id
        if local_data.authorization:
            headers["Authorization"] = local_data.authorization
        if local_data.rur:
            headers["Ig-U-Rur"] = local_data.rur

        if local_data.mid:
            headers["X-Mid"] = local_data.mid

        headers["Ig-Intended-User-Id"] = (
            local_data.user_id if local_data and local_data.user_id else "0"
        )
        headers["X-Ig-Www-Claim"] = (
            local_data.www_claim if local_data and local_data.www_claim else "0"
        )

        headers["User-Agent"] = instagram_app_user_agent_from_android_device_info(
            device_info, version_info
        )

        return headers

    @classmethod
    def bloks_headers(
        cls,
        device_info: MobileClientAndroidDeviceInfo,
        version_info,
        local_data: MobileInstagramClientLocalData,
    ) -> Dict[str, str]:
        """Заголовки для bloks запросов"""

        headers = cls.api_headers(device_info, version_info, local_data)

        headers.update(
            {
                "X-Bloks-Version-Id": version_info.bloks_version_id,
                "X-Bloks-Is-Layout-Rtl": "false",
                "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
                "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
                "X-Bloks-Prism-Colors-Enabled": "true",
                "X-Bloks-Prism-Font-Enabled": "false",
                "X-Bloks-Prism-Indigo-Link-Version": "0",
            }
        )

        return headers
