import logging
from dataclasses import dataclass

from src.domain.android_device_hardware.entities.android_device_hardware import AndroidDeviceHardware
from src.domain.android_device_hardware.repositories.android_device_hardware import AndroidDeviceHardwareRepository

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class GetAndroidDeviceHardwaresQueryResult:
    android_device_specs: list[AndroidDeviceHardware]


class GetAndroidDeviceHardwaresQueryHandler:

    def __init__(
        self,
        repository: AndroidDeviceHardwareRepository,
    ):
        self._repository = repository

    async def __call__(
        self,
    ) -> GetAndroidDeviceHardwaresQueryResult:
        android_device_specs = await self._repository.get_all()
        return GetAndroidDeviceHardwaresQueryResult(
            android_device_specs=android_device_specs,
        )
