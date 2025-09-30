from typing import Protocol
from uuid import UUID


class Logger(Protocol):

    async def info(self, msg, *args, **kwargs): ...

    async def error(self, msg, *args, **kwargs): ...

    async def debug(self, msg, *args, **kwargs): ...

    async def warning(self, msg, *args, **kwargs): ...


class AccountWorkerLogger(Logger):
    def set_account_id(self, account_id: UUID) -> None:...


class AccountWorkerLoggerFactory(Protocol):

    def create(self, account_id: UUID | None = None) -> AccountWorkerLogger: ...
