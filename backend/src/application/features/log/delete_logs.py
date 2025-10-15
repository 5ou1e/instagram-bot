import logging
from uuid import UUID

from src.domain.aggregates.account_worker.repositories.account_worker_log import (
    AccountWorkerLogRepository,
)
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)

DeleteLogsCommandResult = type(None)


class DeleteLogsCommandHandler:

    def __init__(
        self,
        uow: Uow,
        repository: AccountWorkerLogRepository,
    ):
        self._uow = uow
        self._repository = repository

    async def __call__(
        self,
        account_ids: list[UUID] | None = None,
    ) -> DeleteLogsCommandResult:
        async with self._uow:
            await self._repository.bulk_delete(
                account_ids=account_ids,
            )
