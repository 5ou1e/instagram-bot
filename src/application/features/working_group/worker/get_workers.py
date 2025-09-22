import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.dtos.pagination import Pagination
from src.application.common.interfaces.account_worker_reader import AccountWorkerReader
from src.application.features.working_group.worker.dto import WorkingGroupWorkersDTO

logger = logging.getLogger(__name__)


@dataclass
class GetWorkingGroupWorkersQuery:
    working_group_id: UUID
    pagination: Pagination


class GetWorkingGroupWorkersQueryHandler:

    def __init__(
        self,
        reader: AccountWorkerReader,
    ):
        self._reader = reader

    async def __call__(
        self,
        query: GetWorkingGroupWorkersQuery,
    ) -> WorkingGroupWorkersDTO:
        return await self._reader.get_workers_by_working_group(
            query.working_group_id, query.pagination
        )
