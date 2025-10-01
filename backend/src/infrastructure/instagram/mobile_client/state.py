from dataclasses import dataclass

from src.domain.shared.interfaces.instagram.mobile_client.entities.android_device_info import (
    MobileClientAndroidDeviceInfo,
)
from src.domain.shared.interfaces.instagram.mobile_client.entities.local_data import (
    MobileInstagramClientLocalData,
)
from src.infrastructure.instagram.mobile_client.instagram_version_info import (
    InstagramAppVersionInfo,
)


@dataclass(kw_only=True, slots=True)
class MobileInstagramClientState:
    device_info: MobileClientAndroidDeviceInfo
    local_data: MobileInstagramClientLocalData
    version_info: InstagramAppVersionInfo

    def increment_request_stats(self, response_bytes: int, response_time_ms: int):
        # Увеличивавет счетчики связанные с запросами

        self.local_data.requests_count += 1
        self.local_data.total_bytes += response_bytes
        self.local_data.total_time_ms += response_time_ms
