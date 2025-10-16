from uuid import UUID

from sqlalchemy import delete, select, text, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dtos.account_worker import (
    AccountActionStatisticsDTO,
    AccountWorkerDTO,
    AndroidDeviceDTO,
    AndroidDeviceHardwareDTO,
)
from src.application.common.dtos.pagination import Pagination, PaginationResult
from src.application.common.interfaces.account_worker_reader import AccountWorkerReader
from src.application.features.working_group.account_worker.dto import (
    WorkingGroupWorkersDTO,
)
from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.aggregates.account_worker.entities.account_worker.work_state import \
    AccountWorkerWorkState
from src.domain.aggregates.account_worker.entities.android_device import \
    AndroidDeviceInstagramAppData

from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)

from src.infrastructure.database.repositories.android_device import (
    convert_android_device_entity_to_model,
    convert_android_device_model_to_entity,
)
from src.infrastructure.database.repositories.models import AccountWorkerModel
from src.infrastructure.database.repositories.models.common import model_to_dict
from src.infrastructure.database.repositories.proxy import (
    convert_proxy_entity_to_model,
    convert_proxy_model_to_entity,
)


def convert_account_worker_entity_to_model(
    entity: AccountWorker,
) -> AccountWorkerModel:
    return AccountWorkerModel(
        id=entity.id,
        working_group_id=entity.working_group_id,
        account_id=entity.account_id,
        proxy_id=entity.proxy.id if entity.proxy else None,
        android_device_id=entity.android_device.id if entity.android_device else None,
        android_device=(
            convert_android_device_entity_to_model(entity.android_device)
            if entity.android_device
            else None
        ),
        proxy=convert_proxy_entity_to_model(entity.proxy) if entity.proxy else None,
        work_state=entity.work_state,
        status=entity.status,
        last_action_time=entity.last_action_time,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def convert_account_worker_model_to_entity(model: AccountWorkerModel) -> AccountWorker:
    return AccountWorker(
        id=model.id,
        working_group_id=model.working_group_id,
        account_id=model.account_id,
        proxy=convert_proxy_model_to_entity(model.proxy) if model.proxy else None,
        android_device=(
            convert_android_device_model_to_entity(model.android_device)
            if model.android_device
            else None
        ),
        work_state=model.work_state,
        status=model.status,
        last_action_time=model.last_action_time,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class PostgresAccountWorkerRepository(AccountWorkerRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def acquire_by_id(self, worker_id: UUID) -> AccountWorker | None:
        stmt = (
            select(AccountWorkerModel)
            .where(AccountWorkerModel.id == worker_id)
            .with_for_update(of=AccountWorkerModel)  # <- блокируем только эту таблицу
        )
        result = await self._session.execute(stmt)
        model: AccountWorkerModel = result.unique().scalar_one_or_none()

        return convert_account_worker_model_to_entity(model) if model else None

    async def acquire_all_by_working_group(
        self,
        working_group_id,
        skip_locked=False,
    ) -> list[AccountWorker]:
        stmt = (
            select(AccountWorkerModel)
            .where((AccountWorkerModel.working_group_id == working_group_id))
            .with_for_update(of=AccountWorkerModel, skip_locked=skip_locked)
        )
        result = await self._session.execute(stmt)

        models = result.unique().scalars().all()
        return [convert_account_worker_model_to_entity(m) for m in models]

    async def acquire_by_working_group_id_and_worker_id(
        self,
        working_group_id,
        worker_id: UUID,
        skip_locked=False,
    ) -> AccountWorker | None:
        stmt = (
            select(AccountWorkerModel)
            .where(
                (AccountWorkerModel.working_group_id == working_group_id)
                & (AccountWorkerModel.id == worker_id)
            )
            .with_for_update(of=AccountWorkerModel, skip_locked=skip_locked)  # 👈 важно
        )
        result = await self._session.execute(stmt)
        model: AccountWorkerModel | None = result.unique().scalar_one_or_none()

        return convert_account_worker_model_to_entity(model) if model else None

    async def get_by_id(self, oid: UUID) -> AccountWorker | None:
        stmt = select(AccountWorkerModel).where(AccountWorkerModel.id == oid)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return convert_account_worker_model_to_entity(model) if model else None

    async def update_work_state(
        self,
        entity: AccountWorker,
        status: AccountWorkerWorkState,
    ) -> None:
        model = convert_account_worker_entity_to_model(entity)
        stmt = (
            update(AccountWorkerModel)
            .where(AccountWorkerModel.id == model.id)
            .values(work_state=status)
        )
        await self._session.execute(stmt)

    async def get_all_by_working_group_id(
        self, working_group_id: UUID
    ) -> list[AccountWorker]:
        stmt = select(AccountWorkerModel).where(
            AccountWorkerModel.working_group_id == working_group_id
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [convert_account_worker_model_to_entity(m) for m in models]

    async def get_by_working_group_id_and_account_id(
        self, working_group_id: UUID, account_id: UUID
    ) -> AccountWorker | None:
        stmt = select(AccountWorkerModel).where(
            AccountWorkerModel.working_group_id == working_group_id,
            AccountWorkerModel.account_id == account_id,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return convert_account_worker_model_to_entity(model) if model else None

    async def update(self, entity: AccountWorker) -> None:
        model = convert_account_worker_entity_to_model(entity)
        # Добавляем или обновляем (upsert-подобное поведение)
        await self._session.merge(model)


    async def bulk_create(
        self,
        entities: list[AccountWorker],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list:
        if not entities:
            return []

        models = [convert_account_worker_entity_to_model(entity) for entity in entities]

        values = [model_to_dict(m) for m in models]
        stmt = insert(AccountWorkerModel)

        if return_inserted_ids:
            stmt = stmt.returning(AccountWorkerModel.id)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        result = await self._session.execute(stmt, values)

        if return_inserted_ids:
            inserted_ids = [row[0] for row in result.fetchall()]
        else:
            inserted_ids = []

        if return_inserted_ids:
            return inserted_ids
        else:
            return []

    async def bulk_delete_by_working_group_id(
        self,
        working_group_id: UUID,
        worker_ids: list[UUID] | None,
    ) -> int:

        stmt = delete(AccountWorkerModel).where(
            AccountWorkerModel.working_group_id == working_group_id
        )
        if worker_ids is not None:
            stmt = stmt.where(AccountWorkerModel.id.in_(worker_ids))

        result = await self._session.execute(stmt)
        return result.rowcount  # noqa


class PostgresAccountWorkerReader(AccountWorkerReader):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_workers_by_working_group(
        self,
        working_group_id: UUID,
        pagination: Pagination,
    ) -> WorkingGroupWorkersDTO:

        limit, offset = pagination.limit_offset

        # 1. Считаем общее количество
        count_stmt = text(
            """
            SELECT COUNT(*)
            FROM account_worker aw
            WHERE aw.working_group_id = :working_group_id
            """
        )
        total_count_result = await self._session.execute(
            count_stmt, {"working_group_id": working_group_id}
        )
        total_count = total_count_result.scalar_one()

        stmt = text(
            """
                SELECT 
                    aw.id,
                    aw.account_id,
                    aw.working_group_id,
                    aw.created_at AS attached_to_task,
                    aw.work_state,
                    aw.status,
                    aw.last_action_time,
                    a.username,
                    a.password,
                    a.email_username,
                    a.email_password,
                    a.comment,
                    a.action_statistics as action_statistics,
                    a.password_changed_datetime,
                    a.created_at AS account_created_at,
                    
                    p.protocol AS proxy_protocol,
                    p.host AS proxy_host,
                    p.port AS proxy_port,
                    p.username AS proxy_username,
                    p.password AS proxy_password,
                    ll.message AS last_log_message,
                
                    ad.id AS android_device_id,
                    ad.os_version AS android_device_os_version,
                    ad.os_api_level AS android_device_os_api_level,
                    ad.locale AS android_device_locale,
                    ad.timezone AS android_device_timezone,
                    ad.connection_type AS android_device_connection_type,
                    ad.instagram_app_data AS android_device_instagram_app_data,
                    ad.instagram_app_version AS android_device_instagram_app_version,
                    
                    adh.id AS android_hardware_id,
                    adh.name AS android_hardware_name,
                    adh.manufacturer AS android_hardware_manufacturer,
                    adh.brand AS android_hardware_brand,
                    adh.model AS android_hardware_model,
                    adh.device AS android_hardware_device,
                    adh.cpu AS android_hardware_cpu,
                    adh.dpi AS android_hardware_dpi,
                    adh.resolution AS android_hardware_resolution,
                    adh.os_version AS android_hardware_os_version,
                    adh.os_api_level AS android_hardware_os_api_level,
    
                FROM account_worker aw
                JOIN account a ON aw.account_id = a.id
                LEFT JOIN proxy p ON aw.proxy_id = p.id
                LEFT JOIN LATERAL (
                    SELECT message
                    FROM account_worker_log l
                    WHERE l.account_id = a.id AND l.created_at IS NOT NULL
                    ORDER BY l.created_at DESC, l.seq DESC
                    LIMIT 1
                ) ll ON true
                LEFT JOIN android_device ad ON aw.android_device_id = ad.id
                LEFT JOIN android_device_hardware adh ON ad.hardware_id = adh.id
                WHERE aw.working_group_id = :working_group_id
                LIMIT :limit OFFSET :offset
            """
        )

        result = await self._session.execute(
            stmt,
            {
                "working_group_id": working_group_id,
                "limit": limit,
                "offset": offset,
            },
        )
        rows = result.all()

        workers = [self._convert_row_to_dto(row) for row in rows]

        return WorkingGroupWorkersDTO(
            workers=workers,
            pagination=PaginationResult.from_pagination(
                pagination,
                count=len(workers),
                total_count=total_count,
            ),
        )

    def _convert_row_to_dto(self, row) -> AccountWorkerDTO:
        android_device_dto = None
        if row.android_device_id:
            hardware_dto = AndroidDeviceHardwareDTO(
                id=row.android_hardware_id,
                name=row.android_hardware_name,
                manufacturer=row.android_hardware_manufacturer,
                brand=row.android_hardware_brand,
                model=row.android_hardware_model,
                device=row.android_hardware_device,
                cpu=row.android_hardware_cpu,
                dpi=row.android_hardware_dpi,
                resolution=row.android_hardware_resolution,
                os_version=row.android_hardware_os_version,
                os_api_level=row.android_hardware_os_api_level,
            )

            android_device_dto = AndroidDeviceDTO(
                id=row.android_device_id,
                hardware=hardware_dto,
                os_version=row.android_device_os_version,
                os_api_level=row.android_device_os_api_level,
                locale=row.android_device_locale,
                timezone=row.android_device_timezone,
                connection_type=row.android_device_connection_type,
                instagram_app_version=row.android_device_instagram_app_version,
                instagram_app_data=(
                    AndroidDeviceInstagramAppData.from_dict(
                        row.android_device_instagram_app_data
                    )
                    if row.android_device_instagram_app_data
                    else None
                ),
            )

        return AccountWorkerDTO(
            id=row.id,
            account_id=row.account_id,
            working_group_id=row.working_group_id,
            username=row.username,
            password=row.password,
            comment=row.comment,
            email_username=row.email_username,
            email_password=row.email_password,
            android_device=android_device_dto,
            proxy=self._build_proxy_url(row) if row.proxy_host else None,
            action_statistics=AccountActionStatisticsDTO.from_dict(
                row.action_statistics
            ),
            status=row.status,
            last_log_message=row.last_log_message,
            last_action_time=row.last_action_time,
            password_changed_datetime=row.password_changed_datetime,
            created_at=row.account_created_at,
            attached_to_task=row.attached_to_task,
            work_state=AccountWorkerWorkState(row.work_state),
        )

    def _build_proxy_url(self, row) -> str:
        if row.proxy_username and row.proxy_password:
            return f"{row.proxy_protocol}://{row.proxy_username}:{row.proxy_password}@{row.proxy_host}:{row.proxy_port}"
        return f"{row.proxy_protocol}://{row.proxy_host}:{row.proxy_port}"
