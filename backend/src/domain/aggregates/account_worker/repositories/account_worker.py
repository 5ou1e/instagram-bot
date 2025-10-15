from typing import Protocol
from uuid import UUID

from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.aggregates.account_worker.entities.account_worker.work_state import \
    AccountWorkerWorkState


class AccountWorkerRepository(Protocol):

    async def acquire_by_id(
        self,
        worker_id: UUID,
    ) -> AccountWorker | None: ...

    async def acquire_all_by_working_group(
        self,
        working_group_id,
        skip_locked=False,
    ) -> list[AccountWorker]: ...

    async def acquire_by_working_group_id_and_worker_id(
        self,
        working_group_id,
        worker_id: UUID,
        skip_locked=False,
    ) -> AccountWorker | None: ...

    async def get_by_id(self, oid: UUID) -> AccountWorker | None: ...

    async def get_all_by_working_group_id(
        self,
        working_group_id: UUID,
    ) -> list[AccountWorker]: ...

    async def get_by_working_group_id_and_account_id(
        self,
        working_group_id: UUID,
        account_id: UUID,
    ) -> AccountWorker | None: ...

    async def update_work_state(
        self,
        entity: AccountWorker,
        status: AccountWorkerWorkState,
    ) -> None: ...

    async def update(self, entity: AccountWorker) -> None: ...

    async def bulk_create(
        self,
        entities: list[AccountWorker],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list: ...

    async def bulk_delete_by_working_group_id(
        self,
        working_group_id: UUID,
        worker_ids: list[UUID] | None,
    ) -> int: ...
