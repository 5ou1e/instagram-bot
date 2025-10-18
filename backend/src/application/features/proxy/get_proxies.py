import logging
from dataclasses import dataclass

from src.application.common.dtos.pagination import Pagination
from src.application.common.interfaces.proxies_reader import ProxiesReader
from src.application.features.proxy.dto import ProxiesDTO

logger = logging.getLogger(__name__)


@dataclass
class GetProxiesQuery:
    pagination: Pagination


class GetProxiesQueryHandler:

    def __init__(
        self,
        reader: ProxiesReader,
    ):
        self._reader = reader

    async def __call__(
        self,
        query: GetProxiesQuery,
    ) -> ProxiesDTO:
        return await self._reader.get_proxies(query.pagination)
