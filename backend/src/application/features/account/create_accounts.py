import logging
from dataclasses import dataclass
from uuid import UUID

from src.domain.aggregates.account.repository import AccountRepository
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
        raise NotImplementedError
