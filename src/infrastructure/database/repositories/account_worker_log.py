from typing import Optional
from uuid import UUID

from sqlalchemy import asc, delete, desc, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.account_worker.entities.account_worker_log import (
    AccountWorkerLog,
    AccountWorkerLogType,
)
from src.domain.account_worker.repositories.account_worker_log import AccountWorkerLogRepository
from src.infrastructure.database.repositories.models.common import model_to_dict
from src.infrastructure.database.repositories.models.log import AccountWorkerLogModel


def convert_model_to_entity(model: AccountWorkerLogModel) -> AccountWorkerLog:
    return AccountWorkerLog(
        id=model.id,
        level=model.level,
        type=AccountWorkerLogType(model.type),
        seq=model.seq,
        message=model.message,
        account_id=model.account_id,
        created_at=model.created_at,
    )


def convert_entity_to_model(entity: AccountWorkerLog) -> AccountWorkerLogModel:
    return AccountWorkerLogModel(
        id=entity.id,
        level=entity.level,
        type=entity.type.value,
        seq=entity.seq,
        message=entity.message,
        account_id=entity.account_id,
        created_at=entity.created_at,
    )


class PostgresAccountWorkerLogRepository(AccountWorkerLogRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, entity: AccountWorkerLog) -> None:
        log = convert_entity_to_model(entity)
        self._session.add(log)

    async def bulk_create(
        self,
        entities: list[AccountWorkerLog],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[UUID] | None:
        if not entities:
            return []

        models = [convert_entity_to_model(entity) for entity in entities]

        values = [model_to_dict(m) for m in models]

        stmt = insert(AccountWorkerLogModel)

        if return_inserted_ids:
            stmt = stmt.returning(AccountWorkerLogModel.id)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        result = await self._session.execute(stmt, values)

        if return_inserted_ids:
            inserted_ids = [row[0] for row in result.fetchall()]
        else:
            inserted_ids = []

        if return_inserted_ids:
            return inserted_ids

    async def get_all(
        self,
        account_ids: list[UUID] | None = None,
        types: list[AccountWorkerLogType] | None = None,
        sorting: list[str] | None = None,
    ) -> list[AccountWorkerLog]:
        query = select(AccountWorkerLogModel)

        if account_ids:
            query = query.where(AccountWorkerLogModel.account_id.in_(account_ids))

        if types:
            query = query.where(AccountWorkerLogModel.type.in_([t.value for t in types]))

        if sorting:
            for sort_field in sorting:
                if sort_field.startswith("-"):
                    field_name = sort_field[1:]
                    query = query.order_by(desc(getattr(AccountWorkerLogModel, field_name)))
                else:
                    query = query.order_by(asc(getattr(AccountWorkerLogModel, sort_field)))

        result = await self._session.execute(query)
        rows = result.scalars().all()

        return [convert_model_to_entity(row) for row in rows]

    async def bulk_delete(
        self,
        account_ids: Optional[list[UUID]],
    ) -> int:
        stmt = delete(AccountWorkerLogModel)
        if account_ids is not None:
            stmt = stmt.where(AccountWorkerLogModel.account_id.in_(account_ids))

        result = await self._session.execute(stmt)
        return result.rowcount  # noqa
