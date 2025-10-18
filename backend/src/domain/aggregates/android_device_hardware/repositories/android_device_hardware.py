from typing import Protocol
from uuid import UUID

from src.domain.aggregates.android_device_hardware.entities.android_device_hardware import (
    AndroidDeviceHardware,
)


class AndroidDeviceHardwareRepository(Protocol):

    async def get_all(self) -> list[AndroidDeviceHardware]: ...
    async def get_by_id(self, spec_id: UUID) -> AndroidDeviceHardware | None: ...
    async def create(self, entity: AndroidDeviceHardware) -> AndroidDeviceHardware: ...

    async def bulk_create(
        self,
        entities: list[AndroidDeviceHardware],
        on_conflict_do_nothing: bool = False,
    ) -> list[AndroidDeviceHardware] | None: ...

    async def bulk_delete(
        self,
        ids: list[UUID] | None = None,
    ) -> int: ...

    async def delete_all(
        self,
    ) -> int: ...

    async def get_by_unique_keys(
        self,
        unique_keys: list[tuple],
    ) -> list[AndroidDeviceHardware]:
        """Получить все по уникальным ключам"""
        ...
