import logging
from uuid import UUID

from src.domain.imap.repository import IMAPRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)

DeleteIMAPsCommandResult = type(None)


class DeleteIMAPsCommandHandler:

    def __init__(
        self,
        uow: Uow,
        ua_repository: IMAPRepository,
    ):
        self._uow = uow
        self._repository = ua_repository

    async def __call__(
        self,
        ids: list[UUID] | None = None,
    ) -> DeleteIMAPsCommandResult:
        async with self._uow:
            await self._repository.bulk_delete(ids)
