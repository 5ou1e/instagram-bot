import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.converters.account.converter import (
    convert_account_string_to_entity,
)
from src.domain.account.repositories.account import AccountRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class CreateAccountsCommandResult:
    ids: list[UUID]


class CreateAccountsCommandHandler:

    def __init__(
        self,
        uow: Uow,
        account_repository: AccountRepository,
    ):
        self._uow = uow
        self._account_repository = account_repository

    async def __call__(
        self,
        data: list[str],
    ) -> CreateAccountsCommandResult:
        """Добавляем аккаунты в БД"""

        accounts = [convert_account_string_to_entity(line) for line in data]

        created = await self._account_repository.bulk_create(
            accounts,
            on_conflict_do_nothing=True,
            return_inserted_ids=True,
        )

        await self._uow.commit()

        return CreateAccountsCommandResult(
            ids=[acc.id for acc in created],
        )
