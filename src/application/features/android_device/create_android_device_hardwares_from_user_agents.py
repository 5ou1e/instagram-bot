import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.converters.android_device_hardware import (
    android_device_hardware_from_user_agent_string,
)
from src.application.common.exceptions import IncorrectAndroidUserAgentString
from src.domain.android_device.repository import AndroidDeviceHardwareRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class CreateAndroidDeviceHardwaresFromUserAgentsCommandResult:
    created_ids: list[UUID]
    created_count: int
    skipped_count: int


class CreateAndroidDeviceHardwaresFromUserAgentsCommandHandler:
    def __init__(
        self,
        uow: Uow,
        spec_repository: AndroidDeviceHardwareRepository,
    ):
        self._uow = uow
        self._repository = spec_repository

    async def __call__(
        self,
        data: list[str],
    ) -> CreateAndroidDeviceHardwaresFromUserAgentsCommandResult:
        """Создает AndroidDeviceHardware из списка user-agent строк"""
        async with self._uow:
            specs = []
            parse_errors = 0

            for ua_string in data:
                try:
                    spec = android_device_hardware_from_user_agent_string(ua_string)
                    specs.append(spec)
                except IncorrectAndroidUserAgentString as e:
                    logger.warning(
                        f"Failed to parse user-agent: {ua_string}. Error: {e}"
                    )
                    parse_errors += 1
                    continue

            # Убираем дубликаты по unique_key перед отправкой в БД
            unique_specs = list({spec.unique_key: spec for spec in specs}.values())

            created_specs = await self._repository.bulk_create(
                unique_specs,
                on_conflict_do_nothing=True,
            )

            skipped_count = len(unique_specs) - len(created_specs) + parse_errors

            return CreateAndroidDeviceHardwaresFromUserAgentsCommandResult(
                created_ids=[spec.id for spec in created_specs],
                created_count=len(created_specs),
                skipped_count=skipped_count,
            )
