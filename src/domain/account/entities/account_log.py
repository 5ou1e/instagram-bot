from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class AccountWorkerLogType(Enum):
    DEFAULT = "default"
    INSTAGRAM_CLIENT = "instagram_client"


class AccountWorkerLogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    def __init__(self, value):
        self._order = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}[value]

    @property
    def order(self):
        return self._order


@dataclass(kw_only=True, slots=True)
class AccountWorkerLog:
    id: UUID
    account_id: UUID
    level: AccountWorkerLogLevel
    type: AccountWorkerLogType = AccountWorkerLogType.DEFAULT
    seq: int  # Sequence number для упорядочивания
    message: str
    created_at: datetime | None = None
