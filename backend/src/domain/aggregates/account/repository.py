from typing import Optional, Protocol

from uuid6 import UUID

from src.domain.aggregates.account.entities.account import Account


class AccountRepository(Protocol):

    async def acquire_by_id(self, id: UUID, skip_locked=False) -> Account | None: ...
    async def acquire_all(self) -> list[Account]: ...
    async def get_all(self) -> list[Account]: ...
    async def get_by_id(self, account_id: UUID) -> Account | None: ...

    async def get_one(self) -> Account | None: ...

    async def get(self, ids: Optional[list[UUID]] = None) -> list[Account]: ...

    async def get_by_usernames(self, usernames: list[str]) -> list[Account]: ...

    async def create(self, account: Account) -> Account: ...

    async def update(self, account: Account) -> None: ...

    async def bulk_delete(
        self,
        ids: Optional[list[UUID]],
    ) -> int: ...

    async def bulk_create(
        self,
        entities: list[Account],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[Account] | None: ...

    async def get_existing_usernames(
        self,
        usernames: list[str] = None,
    ) -> list[str]: ...
