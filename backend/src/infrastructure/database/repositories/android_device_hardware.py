from uuid import UUID

from sqlalchemy import delete, select, tuple_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.aggregates.android_device_hardware.entities.android_device_hardware import (
    AndroidDeviceHardware,
)
from src.domain.aggregates.android_device_hardware.repositories.android_device_hardware import (
    AndroidDeviceHardwareRepository,
)
from src.infrastructure.database.repositories.models import AndroidDeviceHardwareModel
from src.infrastructure.database.repositories.models.common import model_to_dict


def convert_android_device_hardware_model_to_entity(
        model: AndroidDeviceHardwareModel,
) -> AndroidDeviceHardware:
    return AndroidDeviceHardware(
        id=model.id,
        name=model.name,
        manufacturer=model.manufacturer,
        brand=model.brand,
        model=model.model,
        device=model.device,
        cpu=model.cpu,
        os_version=model.os_version,
        os_api_level=model.os_api_level,
        dpi=model.dpi,
        resolution=model.resolution,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def convert_android_device_hardware_entity_to_model(
        entity: AndroidDeviceHardware,
) -> AndroidDeviceHardwareModel:
    return AndroidDeviceHardwareModel(
        id=entity.id,
        name=entity.name,
        manufacturer=entity.manufacturer,
        brand=entity.brand,
        model=entity.model,
        device=entity.device,
        cpu=entity.cpu,
        os_version=entity.os_version,
        os_api_level=entity.os_api_level,
        dpi=entity.dpi,
        resolution=entity.resolution,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


class PostgresAndroidDeviceHardwareRepository(AndroidDeviceHardwareRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, entity: AndroidDeviceHardware) -> AndroidDeviceHardware:
        model = convert_android_device_hardware_entity_to_model(entity)
        self._session.add(model)
        return entity

    async def get_by_id(self, spec_id: UUID) -> AndroidDeviceHardware | None:
        result = await self._session.execute(
            select(AndroidDeviceHardwareModel).where(
                AndroidDeviceHardwareModel.id == spec_id
            )
        )
        model = result.scalar_one_or_none()
        return convert_android_device_hardware_model_to_entity(model) if model else None

    async def get_by_name(self, name: str) -> AndroidDeviceHardware | None:
        result = await self._session.execute(
            select(AndroidDeviceHardwareModel).where(
                AndroidDeviceHardwareModel.name == name
            )
        )
        model = result.scalar_one_or_none()
        return convert_android_device_hardware_model_to_entity(model) if model else None

    async def get_all(self) -> list[AndroidDeviceHardware]:
        result = await self._session.execute(select(AndroidDeviceHardwareModel))
        models = result.scalars().all()
        return [
            convert_android_device_hardware_model_to_entity(model) for model in models
        ]

    async def bulk_create(
            self,
            entities: list[AndroidDeviceHardware],
            on_conflict_do_nothing: bool = False,
    ) -> list[AndroidDeviceHardware] | None:
        if not entities:
            return []

        models = [
            convert_android_device_hardware_entity_to_model(account)
            for account in entities
        ]
        values = [model_to_dict(m) for m in models]

        stmt = insert(AndroidDeviceHardwareModel).values(values)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        stmt = stmt.returning(AndroidDeviceHardwareModel)

        result = await self._session.execute(stmt)
        created_models = result.scalars().all()

        for account, model in zip(entities, created_models):
            account.id = model.id

        return entities

    async def bulk_delete(self, ids: list[UUID] | None = None) -> int:
        if not ids:
            return 0

        stmt = delete(AndroidDeviceHardwareModel).where(
            AndroidDeviceHardwareModel.id.in_(ids)
        )
        result = await self._session.execute(stmt)
        return result.rowcount  # noqa

    async def delete_all(self) -> int:
        stmt = delete(AndroidDeviceHardwareModel)
        result = await self._session.execute(stmt)
        return result.rowcount  # noqa

    async def get_by_unique_keys(
            self, unique_keys: list[tuple]
    ) -> list[AndroidDeviceHardware]:
        """Получить specs по уникальным ключам"""
        if not unique_keys:
            return []

        stmt = select(AndroidDeviceHardwareModel).where(
            tuple_(
                AndroidDeviceHardwareModel.manufacturer,
                AndroidDeviceHardwareModel.model,
                AndroidDeviceHardwareModel.device,
                AndroidDeviceHardwareModel.resolution,
            ).in_(unique_keys)
        )

        result = await self._session.execute(stmt)

        return [
            convert_android_device_hardware_model_to_entity(m)
            for m in result.scalars().all()
        ]
