from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class InstagramNetworkConfig:
    max_network_wait_time: int = 15
    max_retries_on_network_errors: int = 0
    delay_before_retries_on_network_errors: int = 0
    work_with_proxy: bool = False
    change_proxy_on_network_errors: bool = False
    max_proxy_changes_on_network_errors: int = 1
    delay_before_proxy_changes_on_network_errors: int = 1
