from typing import Optional, Protocol
from uuid import UUID

from src.domain.aggregates.account_worker.entities.android_device import AndroidDevice


class AndroidDeviceRepository(Protocol):

    async def get(
        self,
        device_ids: list[UUID] | None = None,
    ) -> list[AndroidDevice]: ...
    async def get_all(self) -> list[AndroidDevice]: ...

    async def create(self, entity: AndroidDevice) -> AndroidDevice: ...

    async def get_by_id(self, device_id: UUID) -> AndroidDevice | None: ...

    async def bulk_create(
        self,
        entities: list[AndroidDevice],
        on_conflict_do_nothing: bool = False,
    ) -> list[AndroidDevice]: ...

    async def bulk_delete(
        self,
        ids: Optional[list[UUID]],
    ) -> int: ...
