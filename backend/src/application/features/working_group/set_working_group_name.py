from dataclasses import dataclass
from uuid import UUID

from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.exceptions import (
    WorkingGroupWithThisNameAlreadyExistError,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository


@dataclass
class SetWorkingGroupNameCommand:
    working_group_id: UUID
    name: str


class SetWorkingGroupNameCommandHandler:

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository

    async def __call__(
        self,
        command: SetWorkingGroupNameCommand,
    ) -> None:
        working_group_id = command.working_group_id
        name = command.name
        existing_wg_with_this_name = await self._working_group_repository.get_by_name(
            name
        )
        if (
            existing_wg_with_this_name
            and existing_wg_with_this_name.id != working_group_id
        ):
            raise WorkingGroupWithThisNameAlreadyExistError(name=name)

        working_group = await self._working_group_repository.acquire_by_id(
            working_group_id
        )

        working_group.name = name

        await self._working_group_repository.update(working_group)
        await self._uow.commit()
