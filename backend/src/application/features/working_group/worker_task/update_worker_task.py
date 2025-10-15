from dataclasses import dataclass
from typing import Union
from uuid import UUID

from src.application.common.types import UNSET, UnsetType
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.shared.interfaces.uow import Uow


@dataclass
class UpdateWorkingGroupAccountWorkerTaskCommand:
    working_group_id: UUID
    task_id: UUID
    name: Union[str, None, UnsetType] = UNSET
    enabled: Union[bool, None, UnsetType] = UNSET
    index: Union[int, None, UnsetType] = UNSET
    config: Union[dict, None, UnsetType] = UNSET


UpdateWorkingGroupAccountWorkerTaskCommandResult = type(None)


class UpdateWorkingGroupAccountWorkerTaskCommandHandler:
    """Обновить WorkingGroupAccountWorkerTask"""

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository

    async def __call__(
        self,
        command: UpdateWorkingGroupAccountWorkerTaskCommand,
    ) -> UpdateWorkingGroupAccountWorkerTaskCommandResult:
        async with self._uow:
            working_group = await self._working_group_repository.acquire_by_id(
                command.working_group_id
            )

            if command.name is not UNSET:
                working_group.update_account_worker_task_name(
                    command.task_id, command.name
                )
            if command.enabled is not UNSET:
                working_group.update_account_worker_task_enabled(
                    command.task_id, command.enabled
                )
            if command.index is not UNSET:
                working_group.update_account_worker_task_index(
                    command.task_id, command.index
                )
            if command.config is not UNSET:
                working_group.update_account_worker_task_config(
                    command.task_id, command.config
                )

            await self._working_group_repository.update(working_group)
            await self._uow.commit()
