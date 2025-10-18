from typing import Protocol

from src.application.common.dtos.pagination import Pagination
from src.application.features.proxy.dto import ProxiesDTO


class ProxiesReader(Protocol):
    """Выполняет запросы чтения и возвращает DTO обьекты"""

    async def get_proxies(
        self,
        pagination: Pagination,
    ) -> ProxiesDTO: ...
