import logging
from dataclasses import dataclass
from uuid import UUID

from src.domain.account_worker.entities.account_worker_log import (
    AccountWorkerLog,
    AccountWorkerLogType,
)
from src.domain.account_worker.repositories.account_worker_log import AccountWorkerLogRepository

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class GetLogsQueryResult:
    logs: list[AccountWorkerLog]


class GetLogsQueryHandler:

    def __init__(
        self,
        repository: AccountWorkerLogRepository,
    ):
        self._repository = repository

    async def __call__(
        self,
        account_ids: list[UUID] | None = None,
        types: list[AccountWorkerLogType] | None = None,
    ) -> GetLogsQueryResult:
        logs = await self._repository.get_all(
            account_ids=account_ids,
            types=types,
            sorting=["created_at", "seq"],
        )
        return GetLogsQueryResult(
            logs=logs,
        )
