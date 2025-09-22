from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.shared.interfaces.uow import Uow


class SQLAlchemyUoW(Uow):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            raise e

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as e:
            raise e
