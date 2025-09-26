from dataclasses import dataclass
from uuid import UUID

from src.domain.shared.interfaces.uow import Uow

from src.domain.working_group.repositories.working_group import WorkingGroupRepository


@dataclass
class DeleteWorkingGroupWorkerTaskCommand:
    working_group_id: UUID
    task_id: UUID


class DeleteWorkingGroupWorkerTaskCommandHandler:
    """Удалить задачу воркеров рабочей группы"""

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository

    async def __call__(
        self,
        command: DeleteWorkingGroupWorkerTaskCommand,
    ) -> None:
        async with self._uow:
            working_group = await self._working_group_repository.acquire_by_id(
                working_group_id=command.working_group_id
            )
            working_group.delete_worker_task(command.task_id)
            await self._working_group_repository.update(working_group)

