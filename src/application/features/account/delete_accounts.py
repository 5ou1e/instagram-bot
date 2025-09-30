from uuid import UUID

from src.domain.account.repositories.account import AccountRepository
from src.domain.shared.interfaces.uow import Uow

DeleteAccountsCommandResult = type(None)


class DeleteAccountsCommandHandler:

    def __init__(
        self,
        uow: Uow,
        repository: AccountRepository,
    ):
        self._uow = uow
        self._repository = repository

    async def __call__(
        self,
        ids: list[UUID] | None = None,
    ) -> DeleteAccountsCommandResult:
        accounts = []

        if not ids:
            accounts = await self._repository.acquire_all()
            to_delete_ids = [account.id for account in accounts if account.may_delete()]
        else:
            for _id in ids:
                account = await self._repository.acquire_by_id(_id, skip_locked=True)
                if account:
                    accounts.append(account)

            to_delete_ids = [account.id for account in accounts if account.may_delete()]

        async with self._uow:
            await self._repository.bulk_delete(to_delete_ids)

