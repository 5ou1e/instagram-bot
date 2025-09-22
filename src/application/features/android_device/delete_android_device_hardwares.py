import logging
from uuid import UUID

from src.domain.android_device.repository import AndroidDeviceHardwareRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)


class DeleteAndroidDeviceHardwaresCommandHandler:

    def __init__(
        self,
        uow: Uow,
        ua_repository: AndroidDeviceHardwareRepository,
    ):
        self._uow = uow
        self._repository = ua_repository

    async def __call__(
        self,
        ids: list[UUID] | None = None,
    ) -> None:
        async with self._uow:
            if ids is not None:
                await self._repository.bulk_delete(ids)
            else:
                await self._repository.delete_all()
