from typing import Protocol
from uuid import UUID

from src.application.common.dtos.working_group import WorkingGroupDTO, WorkingGroupsDTO


class WorkingGroupReader(Protocol):

    async def get_working_group_by_id(
        self,
        working_group_id: UUID,
        include_worker_tasks: bool = False,
    ) -> WorkingGroupDTO: ...

    async def get_working_groups(
        self,
        include_worker_tasks: bool = False,
    ) -> WorkingGroupsDTO: ...
