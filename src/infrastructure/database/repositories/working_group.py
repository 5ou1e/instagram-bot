from typing import List
from uuid import UUID

from sqlalchemy import case, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.application.common.dtos.working_group import WorkingGroupDTO, WorkingGroupsDTO
from src.application.common.interfaces.working_group_reader import WorkingGroupReader
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.working_group.entities.worker.work_state import AccountWorkerWorkState
from src.domain.working_group.entities.working_group.entity import WorkingGroup
from src.domain.working_group.entities.working_group.work_state import (
    WorkingGroupWorkState,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.infrastructure.database.repositories.models import AccountWorkerModel
from src.infrastructure.database.repositories.models.working_group import (
    WorkingGroupModel,
)
from src.infrastructure.database.repositories.working_group_worker import (
    convert_account_worker_entity_to_model,
    convert_account_worker_model_to_entity,
)
from src.infrastructure.database.repositories.working_group_worker_task import (
    convert_worker_task_entity_to_model,
    convert_worker_task_model_to_entity,
)


def convert_working_group_entity_to_model(entity: WorkingGroup) -> WorkingGroupModel:
    return WorkingGroupModel(
        id=entity.id,
        name=entity.name,
        config=entity.config.model_dump(mode="json"),
        work_state=entity.work_state,
        workers=[convert_account_worker_entity_to_model(ta) for ta in entity.workers],
        worker_tasks=[
            convert_worker_task_entity_to_model(m) for m in entity.worker_tasks
        ],
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def convert_working_group_model_to_entity(model: WorkingGroupModel) -> WorkingGroup:
    return WorkingGroup(
        id=model.id,
        name=model.name,
        config=WorkingGroupConfig.model_validate(model.config),
        work_state=model.work_state,
        workers=(
            [convert_account_worker_model_to_entity(ta) for ta in model.workers]
            if model.workers
            else []
        ),
        worker_tasks=(
            [convert_worker_task_model_to_entity(m) for m in model.worker_tasks]
            if model.worker_tasks
            else []
        ),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class PostgresWorkingGroupRepository(WorkingGroupRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def acquire_by_id(
        self,
        working_group_id: UUID,
        skip_locked=False,
    ) -> WorkingGroup | None:

        stmt = (
            select(WorkingGroupModel)
            .options(selectinload(WorkingGroupModel.workers))
            .options(selectinload(WorkingGroupModel.worker_tasks))
            .where(WorkingGroupModel.id == working_group_id)
            .with_for_update(
                of=WorkingGroupModel, skip_locked=skip_locked
            )  # блокируем только AccountModel
        )
        # Отдельно лочим связи TaskAccount
        stmt_ta = (
            select(AccountWorkerModel)
            .where(AccountWorkerModel.working_group_id == working_group_id)
            .with_for_update(skip_locked=skip_locked)
        )
        result_ta = await self._session.execute(stmt_ta)

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return convert_working_group_model_to_entity(model) if model else None

    async def get_by_name(self, name: str) -> WorkingGroup | None:
        stmt = select(WorkingGroupModel).where(WorkingGroupModel.name == name)
        result = await self._session.execute(stmt)
        task = result.unique().scalar_one_or_none()

        return convert_working_group_model_to_entity(task) if task else None

    async def get(self) -> List[WorkingGroup]:
        stmt = select(WorkingGroupModel)
        result = await self._session.execute(stmt)
        records = result.unique().scalars().all()
        return [convert_working_group_model_to_entity(record) for record in records]

    async def get_all(self) -> List[WorkingGroup]:
        stmt = select(WorkingGroupModel)
        result = await self._session.execute(stmt)
        records = result.scalars().all()
        return [convert_working_group_model_to_entity(record) for record in records]

    async def get_by_id(self, working_group_id: UUID) -> WorkingGroup | None:
        stmt = (
            select(WorkingGroupModel)
            .where(WorkingGroupModel.id == working_group_id)
            .options(selectinload(WorkingGroupModel.worker_tasks))
        )

        result = await self._session.execute(stmt)

        model = result.scalars().unique().one_or_none()

        return convert_working_group_model_to_entity(model) if model else None

    async def create(self, entity: WorkingGroup) -> WorkingGroup:
        model = convert_working_group_entity_to_model(entity)
        self._session.add(model)
        return entity

    async def update(self, entity: WorkingGroup) -> None:
        model = convert_working_group_entity_to_model(entity)
        await self._session.merge(model)

    async def delete(self, working_group_id: UUID) -> None:
        stmt = delete(WorkingGroupModel).where(WorkingGroupModel.id == working_group_id)
        await self._session.execute(stmt)


class PostgresWorkingGroupReader(WorkingGroupReader):
    """Выполняет запросы чтения и возвращает DTO обьекты"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_working_group_by_id(
        self,
        working_group_id: UUID,
        include_worker_tasks: bool = False,
    ) -> WorkingGroupDTO:
        stmt = select(WorkingGroupModel).where(WorkingGroupModel.id == working_group_id)
        if include_worker_tasks:
            stmt = stmt.options(selectinload(WorkingGroupModel.worker_tasks))

        result = await self._session.execute(stmt)
        model = result.scalars().unique().one_or_none()
        if model is None:
            return None

        # Группировка по состояниям воркеров
        count_stmt = select(
            func.count(case((AccountWorkerModel.work_state == "IDLE", 1))).label(
                "idle"
            ),
            func.count(
                case(
                    (AccountWorkerModel.work_state == AccountWorkerWorkState.WORKING, 1)
                )
            ).label("working"),
            func.count(
                case(
                    (
                        AccountWorkerModel.work_state
                        == AccountWorkerWorkState.STOPPING,
                        1,
                    )
                )
            ).label("stopping"),
            func.count(
                case(
                    (
                        AccountWorkerModel.work_state
                        == AccountWorkerWorkState.STARTING,
                        1,
                    )
                )
            ).label("starting"),
        ).where(AccountWorkerModel.working_group_id == working_group_id)

        count_result = await self._session.execute(count_stmt)
        counts = count_result.one()

        return WorkingGroupDTO(
            id=model.id,
            work_state=WorkingGroupWorkState(model.work_state),
            name=model.name,
            config=model.config,
            worker_tasks=(
                [convert_worker_task_model_to_entity(st) for st in model.worker_tasks]
                if include_worker_tasks
                else []
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
            working_workers_count=counts.working,
            starting_workers_count=counts.starting,
            stopping_workers_count=counts.stopping,
            idle_workers_count=counts.idle,
        )

    async def get_working_groups(
        self, include_worker_tasks: bool = True
    ) -> WorkingGroupsDTO:

        stmt = select(WorkingGroupModel)
        if include_worker_tasks:
            stmt = stmt.options(selectinload(WorkingGroupModel.worker_tasks))

        result = await self._session.execute(stmt)

        models = result.unique().scalars().all()

        dtos = [
            WorkingGroupDTO(
                id=model.id,
                work_state=WorkingGroupWorkState(model.work_state),
                config=model.config,
                name=model.name,
                worker_tasks=[
                    convert_worker_task_model_to_entity(st) for st in model.worker_tasks
                ],
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
            for model in models
        ]

        return WorkingGroupsDTO(working_groups=dtos)
