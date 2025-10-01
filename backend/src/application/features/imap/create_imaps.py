import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.converters.imap import convert_imap_line_to_entity
from src.domain.imap.repository import IMAPRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class CreateIMAPsCommandResult:
    ids: list[UUID]


class CreateIMAPsCommandHandler:

    def __init__(
        self,
        uow: Uow,
        repository: IMAPRepository,
    ):
        self._uow = uow
        self._repository = repository

    async def __call__(
        self,
        data: list[str],
    ) -> CreateIMAPsCommandResult:
        """Добавляем в БД"""

        imaps = [convert_imap_line_to_entity(line) for line in data]

        async with self._uow:
            created_ids = await self._repository.bulk_create(
                imaps,
                on_conflict_do_nothing=True,
                return_inserted_ids=True,
            )
            return CreateIMAPsCommandResult(
                ids=created_ids,
            )
