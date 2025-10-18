from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.aggregates.account_worker.entities.android_device import AndroidDevice, \
    AndroidDeviceInstagramAppData
from src.domain.aggregates.account_worker.repositories.android_device import (
    AndroidDeviceRepository,
)
from src.infrastructure.database.repositories.android_device_hardware import (
    convert_android_device_hardware_entity_to_model,
    convert_android_device_hardware_model_to_entity,
)
from src.infrastructure.database.repositories.models.android_device import (
    AndroidDeviceModel,
)
from src.infrastructure.database.repositories.models.common import model_to_dict


def convert_android_device_entity_to_model(entity: AndroidDevice) -> AndroidDeviceModel:
    return AndroidDeviceModel(
        id=entity.id,
        hardware_id=entity.hardware.id if entity.hardware else None,
        hardware=(
            convert_android_device_hardware_entity_to_model(entity.hardware)
            if entity.hardware
            else None
        ),
        os_version=entity.os_version,
        os_api_level=entity.os_api_level,
        locale=entity.locale,
        timezone=entity.timezone,
        connection_type=entity.connection_type,
        instagram_app_version=entity.instagram_app_version,
        instagram_app_data=entity.instagram_app_data.to_dict(),
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def convert_android_device_model_to_entity(model: AndroidDeviceModel) -> AndroidDevice:
    return AndroidDevice(
        id=model.id,
        hardware=(
            convert_android_device_hardware_model_to_entity(model.hardware)
            if model.hardware
            else None
        ),
        os_version=model.os_version,
        os_api_level=model.os_api_level,
        locale=model.locale,
        timezone=model.timezone,
        connection_type=model.connection_type,
        instagram_app_version=model.instagram_app_version,
        instagram_app_data=AndroidDeviceInstagramAppData(**model.instagram_app_data),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class PostgresAndroidDeviceRepository(AndroidDeviceRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, entity: AndroidDevice) -> AndroidDevice:
        model = convert_android_device_entity_to_model(entity)
        self._session.add(model)
        await self._session.refresh(model)
        return convert_android_device_model_to_entity(model)

    async def get_by_id(self, device_id: UUID) -> AndroidDevice | None:
        result = await self._session.execute(
            select(AndroidDeviceModel).where(AndroidDeviceModel.id == device_id)
        )
        model = result.scalar_one_or_none()
        return convert_android_device_model_to_entity(model) if model else None

    async def get_all(self) -> list[AndroidDevice]:
        result = await self._session.execute(select(AndroidDeviceModel))
        models = result.scalars().all()
        return [convert_android_device_model_to_entity(model) for model in models]

    async def get(
            self,
            device_ids: list[UUID] | None = None,
    ) -> list[AndroidDevice]:
        stmt = select(AndroidDeviceModel)
        if device_ids:
            stmt = stmt.where(AndroidDeviceModel.id.in_(device_ids))

        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [convert_android_device_model_to_entity(model) for model in models]

    async def bulk_create(
            self,
            entities: list[AndroidDevice],
            on_conflict_do_nothing: bool = False,
    ) -> list[AndroidDevice]:
        if not entities:
            return []

        models = [convert_android_device_entity_to_model(entity) for entity in entities]
        values = [model_to_dict(obj) for obj in models]

        # raise ValueError('asdf')
        stmt = insert(AndroidDeviceModel).values(values)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        stmt = stmt.returning(AndroidDeviceModel)

        result = await self._session.execute(stmt)
        created_models = result.unique().scalars().all()

        # Обновляем id в исходных объектах
        for account, model in zip(entities, created_models):
            account.id = model.id

        return entities

    async def bulk_delete(self, ids: list[UUID] | None = None) -> int:
        if not ids:
            return 0

        stmt = delete(AndroidDeviceModel).where(AndroidDeviceModel.id.in_(ids))
        result = await self._session.execute(stmt)
        return result.rowcount  # noqa
