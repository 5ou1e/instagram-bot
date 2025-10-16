from dataclasses import dataclass
from uuid import UUID

from src.domain.aggregates.account.repository import AccountRepository
from src.domain.shared.interfaces.uow import Uow


@dataclass(kw_only=True, slots=True)
class SetAccountsCommentCommand:
    account_ids: list[UUID]
    comment: str | None = None


class SetAccountsCommentCommandHandler:
    # Установить одинаковый комментарий списку аккаунтов

    def __init__(
        self,
        uow: Uow,
        repository: AccountRepository,
    ):
        self._uow = uow
        self._repository = repository

    async def __call__(
        self,
        command: SetAccountsCommentCommand,
    ) -> None:
        async with self._uow:
            accounts = await self._repository.acquire_by_ids(command.account_ids)
            for account in accounts:
                account.set_comment(command.comment)
                await self._repository.update(account)
