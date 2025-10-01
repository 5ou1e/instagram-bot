import logging

from uuid6 import uuid7

from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)
from src.domain.working_group.entities.working_group.entity import WorkingGroup
from src.domain.working_group.exceptions import WorkingGroupNameAlreadyExistsError
from src.domain.working_group.repositories.working_group import WorkingGroupRepository

logger = logging.getLogger(__name__)


CreateWorkingGroupCommandResult = type(None)


class CreateWorkingGroupCommandHandler:

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository

    async def __call__(self, name: str) -> CreateWorkingGroupCommandResult:
        if await self._working_group_repository.get_by_name(name):
            raise WorkingGroupNameAlreadyExistsError()

        working_group_id = uuid7()
        default_tasks = [
            AccountWorkerTask(
                id=uuid7(),
                type=AccountWorkerTaskType.AUTHORIZE_ACCOUNT,
                name="Авторизация",
                enabled=True,
                index=0,
                config={},
                working_group_id=working_group_id,
            ),
            AccountWorkerTask(
                id=uuid7(),
                type=AccountWorkerTaskType.DO_TASKS_FROM_BOOST_SERVICES,
                name="Задания с сервисов",
                enabled=True,
                index=1,
                config={},
                working_group_id=working_group_id,
            ),
        ]

        working_group = WorkingGroup(
            id=working_group_id, name=name, worker_tasks=default_tasks
        )

        await self._working_group_repository.create(working_group)

        await self._uow.commit()

        return CreateWorkingGroupCommandResult()
