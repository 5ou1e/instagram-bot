from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aiohttp

from src.domain.proxy.entities import Proxy


class HttpSession:
    def __init__(
        self,
        aiohttp_session: aiohttp.ClientSession,
        proxy: Proxy | None = None,
    ):
        self._aiohttp_session = aiohttp_session
        self._proxy: Proxy | None = None
        if proxy:
            self.set_proxy(proxy)

    async def close(self) -> None:
        await self._aiohttp_session.close()

    @property
    def proxy(self):
        return self._proxy

    def set_proxy(self, proxy: Proxy):
        self._proxy = proxy.url if proxy else None

    @asynccontextmanager
    async def request(
        self, method: str, url: str, **kwargs
    ) -> AsyncGenerator[aiohttp.ClientResponse, None]:
        if self._proxy and "proxy" not in kwargs:
            kwargs["proxy"] = self._proxy

        async with self._aiohttp_session.request(method, url, **kwargs) as response:
            yield response
