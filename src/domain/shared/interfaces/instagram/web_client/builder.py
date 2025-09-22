from typing import Protocol, runtime_checkable

from src.domain.account.entities.account import Account
from src.domain.shared.interfaces.instagram.instagram_network_config import (
    InstagramNetworkConfig,
)
from src.domain.shared.interfaces.logger import Logger


@runtime_checkable
class WebInstagramClientBuilder(Protocol):

    def build(
        self,
        account: Account,
        logger: Logger,
        network_config: InstagramNetworkConfig,
    ) -> "WebInstagramClient": ...
