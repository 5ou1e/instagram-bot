from typing import Optional, Protocol
from uuid import UUID

from src.domain.proxy.entities import Proxy


class ProxyRepository(Protocol):
    async def get_random(self) -> Proxy | None: ...

    async def get_all(self) -> list[Proxy]: ...

    async def create(self, entity: Proxy) -> Proxy: ...
    async def bulk_create(
        self,
        entities: list[Proxy],
        on_conflict_do_nothing: bool = False,
    ) -> list[Proxy] | None: ...

    async def bulk_delete(
        self,
        ids: Optional[list[UUID]],
    ) -> int: ...

    async def acquire_least_used(self) -> Proxy | None: ...

    async def update(self, entity: Proxy) -> None: ...

    async def get_by_unique_keys(
        self,
        unique_keys: list[tuple],
    ) -> list[Proxy]:
        """Получить specs по уникальным ключам"""
        ...
