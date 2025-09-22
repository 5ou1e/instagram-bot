from typing import Protocol, runtime_checkable

from src.domain.shared.interfaces.instagram.mobile_client.config import (
    MobileInstagramClientNetworkConfig,
)
from src.domain.shared.interfaces.logger import Logger


@runtime_checkable
class MobileInstagramClientBuilder(Protocol):
    @classmethod
    def new(cls) -> "MobileInstagramClientBuilder": ...

    def with_device_info(
        self,
        device_info: "MobileClientAndroidDeviceInfo",
    ) -> "MobileInstagramClientBuilder": ...

    def with_local_data(
        self,
        local_data: "MobileInstagramClientLocalData",
    ) -> "MobileInstagramClientBuilder": ...

    def with_logger(self, logger: Logger) -> "MobileInstagramClientBuilder": ...

    def with_network_config(
        self, network_config: MobileInstagramClientNetworkConfig
    ) -> "MobileInstagramClientBuilder": ...

    def build(
        self,
    ) -> "MobileInstagramClient": ...
