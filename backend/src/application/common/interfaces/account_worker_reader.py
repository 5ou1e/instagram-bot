from typing import Protocol
from uuid import UUID

from src.application.common.dtos.pagination import Pagination
from src.application.features.working_group.account_worker.dto import (
    WorkingGroupWorkersDTO,
)


class AccountWorkerReader(Protocol):
    """Выполняет запросы чтения и возвращает DTO обьекты"""

    async def get_workers_by_working_group(
        self,
        working_group_id: UUID,
        pagination: Pagination,
    ) -> WorkingGroupWorkersDTO: ...
