from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType
from uuid import UUID

from mashumaro import DataClassDictMixin

from src.domain.aggregates.account.value_objects import Email
from src.domain.aggregates.account_worker.entities.account_worker.work_state import (
    AccountWorkerWorkState,
)
from src.domain.shared.utils import current_datetime

AccountID = NewType("AccountID", UUID)


@dataclass(kw_only=True, slots=True)
class AccountActionStatistics(DataClassDictMixin):
    follows: int = 0
    follows_blocks: int = 0
    authorizations: int = 0


@dataclass(kw_only=True, slots=True)
class Account(DataClassDictMixin):
    id: AccountID
    username: str
    password: str | None = None
    email: Email | None = None
    user_id: int | None = None

    action_statistics: AccountActionStatistics = field(
        default_factory=AccountActionStatistics
    )

    status: str | None = None
    last_action_time: datetime | None = None
    password_changed_datetime: datetime | None = None

    created_at: datetime | None = field(default_factory=current_datetime)
    updated_at: datetime | None = field(default_factory=current_datetime)

    def set_password(self, password: str) -> None:
        self.password = password

    def set_user_id(self, user_id: int):
        self.user_id = user_id

    def set_email(self, email: Email) -> None:
        self.email = email

    def may_delete(self) -> bool:
        if self.worker.work_state != AccountWorkerWorkState.IDLE:
            return False
        return True
