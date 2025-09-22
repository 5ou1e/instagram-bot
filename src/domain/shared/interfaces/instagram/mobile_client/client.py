from typing import Protocol, runtime_checkable

from src.domain.proxy.entities import Proxy
from src.domain.shared.interfaces.instagram.mobile_client.entities.local_data import (
    MobileInstagramClientLocalData,
)


@runtime_checkable
class MobileInstagramClient(Protocol):
    """Интерфейс клиента моб.версии Instagram"""

    test_auth: "TestAuthSection"
    auth: "AuthSection"
    user: "UserSection"
    feed: "FeedSection"
    direct: "DirectSection"
    launcher: "LauncherSection"
    notifications: "NotificationsSection"
    news: "NewsSection"
    media: "MediaSection"
    live: "LiveSection"

    async def __aenter__(self) -> "MobileInstagramClient": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    async def close(self): ...

    def set_proxy(self, proxy: Proxy) -> None: ...

    def get_local_data(self) -> MobileInstagramClientLocalData: ...
