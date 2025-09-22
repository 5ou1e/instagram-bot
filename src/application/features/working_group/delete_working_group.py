from uuid import UUID

from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.repositories.working_group import WorkingGroupRepository

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
