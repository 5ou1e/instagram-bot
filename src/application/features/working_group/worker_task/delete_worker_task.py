from dataclasses import dataclass
from uuid import UUID

from src.application.features.working_group.delete_working_group import (
    DeleteWorkingGroupCommandResult,
)
from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.exceptions import WorkingGroupIdDoesNotExistError
from src.domain.working_group.repositories.account_worker_task import (
    AccountWorkerTaskRepository,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository


@dataclass
class DeleteWorkingGroupWorkerTaskCommand:
    working_group_id: UUID
    subtask_id: UUID


class DeleteWorkingGroupWorkerTaskCommandHandler:
    """Удалить задачу воркеров рабочей группы"""

    def __init__(
        self,
        uow: Uow,
        repository: WorkingGroupRepository,
        account_worker_task_repository: AccountWorkerTaskRepository,
    ):
        self._uow = uow
        self._repository = repository
        self._account_worker_task_repository = account_worker_task_repository

    async def __call__(
        self,
        command: DeleteWorkingGroupWorkerTaskCommand,
    ) -> DeleteWorkingGroupCommandResult:
        async with self._uow:
            task = await self._repository.acquire_by_id(
                working_group_id=command.working_group_id
            )
            if not task:
                raise WorkingGroupIdDoesNotExistError(
                    working_group_id=command.working_group_id
                )

            await self._account_worker_task_repository.delete(command.subtask_id)
