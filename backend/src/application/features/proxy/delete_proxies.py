import logging
from uuid import UUID

from src.domain.aggregates.proxy.repository import ProxyRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)

DeleteProxiesCommandResult = type(None)


class DeleteProxiesCommandHandler:

    def __init__(
        self,
        uow: Uow,
        repository: ProxyRepository,
    ):
        self._uow = uow
        self._repository = repository

    async def __call__(
        self,
        ids: list[UUID] | None = None,
    ) -> DeleteProxiesCommandResult:
        async with self._uow:
            await self._repository.bulk_delete(ids)
