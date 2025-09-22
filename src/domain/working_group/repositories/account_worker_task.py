from typing import List, Protocol
from uuid import UUID

from src.domain.working_group.entities.worker_task.base import AccountWorkerTask


class AccountWorkerTaskRepository(Protocol):

    async def acquire_by_id(self, subtask_id: UUID) -> AccountWorkerTask | None: ...
    async def get_all(self) -> List[AccountWorkerTask]: ...

    async def get_by_id(self, subtask_id: UUID) -> AccountWorkerTask | None: ...

    async def create(self, entity: AccountWorkerTask) -> AccountWorkerTask: ...

    async def delete(self, subtask_id: UUID) -> None: ...

    async def bulk_create(
        self,
        entities: list[AccountWorkerTask],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[UUID] | None: ...

    async def update(self, subtask: AccountWorkerTask) -> None: ...
