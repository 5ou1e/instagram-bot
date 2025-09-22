import logging
from dataclasses import dataclass, field
from typing import Any

from uuid6 import UUID, uuid7

from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.utils import current_datetime
from src.domain.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)
from src.domain.working_group.exceptions import (
    WorkerTaskNameAlreadyExistsError,
    WorkingGroupIdDoesNotExistError,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class CreateWorkerTaskCommand:
    working_group_id: UUID
    type: AccountWorkerTaskType

    # Опциональные поля
    name: str | None = None
    enabled: bool = False
    index: int | None = None
    config: dict[str, Any] = field(default_factory=dict)


class CreateWorkerTaskCommandHandler:

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository

    async def __call__(self, command: CreateWorkerTaskCommand) -> None:
        async with self._uow:
            working_group = await self._working_group_repository.acquire_by_id(
                command.working_group_id
            )
            if not working_group:
                raise WorkingGroupIdDoesNotExistError(
                    working_group_id=command.working_group_id
                )

            name = command.name

            for subtask in working_group.worker_tasks:
                if subtask.name == name:
                    raise WorkerTaskNameAlreadyExistsError(name=name)

            if command.index is None:
                existing_indices = [
                    st.index
                    for st in working_group.worker_tasks
                    if st.index is not None
                ]
                index = max(existing_indices, default=0) + 1
            else:
                index = command.index

            subtask = AccountWorkerTask(
                id=uuid7(),
                type=command.type,
                name=name,
                enabled=command.enabled,
                index=index,
                config=command.config,
                working_group_id=command.working_group_id,
                created_at=current_datetime(),
                updated_at=current_datetime(),
            )

            working_group.worker_tasks.append(subtask)

            await self._working_group_repository.update(working_group)
