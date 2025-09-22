from typing import Optional, Protocol
from uuid import UUID

from src.domain.android_device.entities import AndroidDevice, AndroidDeviceHardware


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


class AndroidDeviceHardwareRepository(Protocol):

    async def get_all(self) -> list[AndroidDeviceHardware]: ...
    async def get_by_id(self, spec_id: UUID) -> AndroidDeviceHardware | None: ...
    async def get_by_name(self, name: str) -> AndroidDeviceHardware | None: ...
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
        """Получить specs по уникальным ключам"""
        ...
