from types import TracebackType
from typing import Protocol, Type


class Uow(Protocol):

    async def __aenter__(self) -> "Uow": ...

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
