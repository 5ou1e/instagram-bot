import logging
from dataclasses import dataclass

from src.domain.proxy.entities import Proxy
from src.domain.proxy.repository import ProxyRepository

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class GetProxiesQueryResult:
    proxies: list[Proxy]


class GetProxiesQueryHandler:

    def __init__(
        self,
        repository: ProxyRepository,
    ):
        self._repository = repository

    async def __call__(
        self,
    ) -> GetProxiesQueryResult:
        proxies = await self._repository.get_all()
        return GetProxiesQueryResult(
            proxies=proxies,
        )
