from typing import Optional, Protocol
from uuid import UUID

from src.domain.imap.entities import IMAP


class IMAPRepository(Protocol):

    async def get_all(self) -> list[IMAP]: ...

    async def get_by_domain(self, domain: str) -> Optional[IMAP]: ...

    async def create(self, entity: IMAP) -> IMAP: ...

    async def bulk_create(
        self,
        entities: list[IMAP],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[UUID] | None: ...

    async def bulk_delete(
        self,
        ids: Optional[list[UUID]],
    ) -> int: ...
