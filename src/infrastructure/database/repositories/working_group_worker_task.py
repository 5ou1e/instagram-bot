from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.working_group.entities.worker_task.base import AccountWorkerTask
from src.domain.working_group.repositories.account_worker_task import (
    AccountWorkerTaskRepository,
)
from src.infrastructure.database.repositories.models import AccountWorkerTaskModel
from src.infrastructure.database.repositories.models.common import model_to_dict


def convert_worker_task_entity_to_model(
    entity: AccountWorkerTask,
) -> AccountWorkerTaskModel:
    return AccountWorkerTaskModel(
        id=entity.id,
        type=entity.type,
        name=entity.name,
        enabled=entity.enabled,
        index=entity.index,
        config=entity.config,
        working_group_id=entity.working_group_id,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def convert_worker_task_model_to_entity(
    model: AccountWorkerTaskModel,
) -> AccountWorkerTask:
    return AccountWorkerTask(
        id=model.id,
        type=model.type,
        name=model.name,
        enabled=model.enabled,
        index=model.index,
        config=model.config or {},
        working_group_id=model.working_group_id,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class PostgresAccountWorkerTaskRepository(AccountWorkerTaskRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def acquire_by_id(self, subtask_id: UUID) -> AccountWorkerTask | None:
        stmt = (
            select(AccountWorkerTaskModel)
            .where(AccountWorkerTaskModel.id == subtask_id)
            .with_for_update()
        )
        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return convert_worker_task_model_to_entity(model) if model else None

    async def get_all(self) -> List[AccountWorkerTask]:
        stmt = select(AccountWorkerTaskModel)
        result = await self._session.execute(stmt)
        records = result.scalars().all()
        return [convert_worker_task_model_to_entity(model) for model in records]

    async def get_by_id(self, subtask_id: UUID) -> AccountWorkerTask | None:
        model = await self._session.get(AccountWorkerTaskModel, subtask_id)
        return convert_worker_task_model_to_entity(model) if model else None

    async def create(self, entity: AccountWorkerTask) -> AccountWorkerTask:
        model = convert_worker_task_entity_to_model(entity)
        self._session.add(model)
        return entity

    async def delete(self, subtask_id: UUID) -> None:
        subtask = await self._session.get(AccountWorkerTaskModel, subtask_id)
        if subtask:
            await self._session.delete(subtask)

    async def bulk_create(
        self,
        entities: list[AccountWorkerTask],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[UUID] | None:
        if not entities:
            return []
        models = [convert_worker_task_entity_to_model(entity) for entity in entities]
        values = [model_to_dict(obj) for obj in models]
        stmt = insert(AccountWorkerTaskModel)

        if return_inserted_ids:
            stmt = stmt.returning(AccountWorkerTaskModel.id)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        result = await self._session.execute(stmt, values)

        if return_inserted_ids:
            return [row[0] for row in result.fetchall()]

    async def update(self, subtask: AccountWorkerTask) -> None:
        model = convert_worker_task_entity_to_model(subtask)
        await self._session.merge(model)
