from dataclasses import dataclass

from src.domain.proxy.entities import Proxy


@dataclass
class MobileInstagramClientNetworkConfig:
    proxy: Proxy | None = None
    max_network_wait_time: float = 0.0
    max_retries_on_network_errors: int = 0
    delay_before_retries_on_network_errors: float = 0.0
