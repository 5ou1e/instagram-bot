from typing import Optional, Protocol
from uuid import UUID

from src.domain.aggregates.account_worker.entities.account_worker_log import (
    AccountWorkerLog,
    AccountWorkerLogType,
)


class AccountWorkerLogRepository(Protocol):

    async def create(self, entity: AccountWorkerLog) -> None: ...

    async def bulk_create(
        self,
        entities: list[AccountWorkerLog],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[UUID] | None: ...

    async def get_all(
        self,
        account_ids: list[UUID] | None = None,
        types: list[AccountWorkerLogType] | None = None,
        sorting: list[str] | None = None,
    ) -> list[AccountWorkerLog]: ...

    async def bulk_delete(
        self,
        account_ids: Optional[list[UUID]],
    ) -> int: ...
