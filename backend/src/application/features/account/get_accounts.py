from dataclasses import dataclass

from src.domain.account.entities.account import Account
from src.domain.account.repositories.account import AccountRepository


@dataclass(kw_only=True, slots=True)
class GetAccountsQueryResult:
    accounts: list[Account]


class GetAccountsQueryHandler:

    def __init__(
        self,
        repository: AccountRepository,
    ):
        self._repository = repository

    async def __call__(
        self,
    ) -> GetAccountsQueryResult:
        accounts = await self._repository.get()
        return GetAccountsQueryResult(
            accounts=accounts,
        )
