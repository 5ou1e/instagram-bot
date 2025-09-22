import logging
from dataclasses import dataclass
from uuid import UUID

from src.domain.account.entities.account_log import (
    AccountWorkerLog,
    AccountWorkerLogType,
)
from src.domain.account.repositories.account_log import LogRepository

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class GetLogsQueryResult:
    logs: list[AccountWorkerLog]


class GetLogsQueryHandler:

    def __init__(
        self,
        repository: LogRepository,
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
