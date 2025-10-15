from uuid import UUID

from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.shared.interfaces.uow import Uow

DeleteWorkingGroupCommandResult = type(None)


class DeleteWorkingGroupCommandHandler:

    def __init__(
        self,
        uow: Uow,
        repository: WorkingGroupRepository,
    ):
        self._uow = uow
        self._repository = repository

    async def __call__(
        self,
        working_group_id: UUID,
    ) -> DeleteWorkingGroupCommandResult:
        # TODO добавить проверку, можно ли удалять задачу
        await self._repository.delete(working_group_id)
        await self._uow.commit()
