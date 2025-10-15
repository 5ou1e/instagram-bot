import logging
from dataclasses import dataclass

from src.domain.aggregates.imap.entities import IMAP
from src.domain.aggregates.imap.repository import IMAPRepository

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class GetIMAPsQueryResult:
    imaps: list[IMAP]


class GetIMAPsQueryHandler:

    def __init__(
        self,
        repository: IMAPRepository,
    ):
        self._repository = repository

    async def __call__(
        self,
    ) -> GetIMAPsQueryResult:
        imaps = await self._repository.get_all()
        return GetIMAPsQueryResult(
            imaps=imaps,
        )
