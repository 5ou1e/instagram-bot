from copy import deepcopy
from dataclasses import dataclass
from uuid import UUID

from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.working_group.exceptions import WorkingGroupIdDoesNotExistError
from src.domain.working_group.repositories.working_group import WorkingGroupRepository


@dataclass
class UpdateWorkingGroupConfigCommand:
    working_group_id: UUID
    data: dict


UpdateWorkingGroupConfigCommandResult = type(None)


class UpdateWorkingGroupConfigCommandHandler:
    """Обновить конфиг рабочей группы"""

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository

    async def __call__(
        self,
        command: UpdateWorkingGroupConfigCommand,
    ) -> UpdateWorkingGroupConfigCommandResult:
        async with self._uow:
            working_group = await self._working_group_repository.get_by_id(
                command.working_group_id
            )
            if not working_group:
                raise WorkingGroupIdDoesNotExistError(
                    working_group_id=command.working_group_id
                )

            current = working_group.config.model_dump()
            patch_data = command.data

            merged = deep_update(deepcopy(current), patch_data)

            new_config = WorkingGroupConfig.model_validate(merged)
            working_group.config = new_config

            # return
            await self._working_group_repository.update(working_group)


def deep_update(orig: dict, patch: dict) -> dict:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(orig.get(k), dict):
            deep_update(orig[k], v)
        else:
            orig[k] = v
    return orig
