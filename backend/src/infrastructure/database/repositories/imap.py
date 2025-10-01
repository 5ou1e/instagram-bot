from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.imap.entities import IMAP
from src.domain.imap.repository import IMAPRepository
from src.infrastructure.database.repositories.models.common import model_to_dict
from src.infrastructure.database.repositories.models.imap import IMAPModel


def convert_imap_entity_to_model(entity: IMAP) -> IMAPModel:
    return IMAPModel(
        id=entity.id,
        domain=entity.domain,
        host=entity.host,
        port=entity.port,
    )


def convert_imap_model_to_entity(model: IMAPModel) -> IMAP:
    return IMAP(
        id=model.id,
        domain=model.domain,
        host=model.host,
        port=model.port,
    )


class PostgresIMAPRepository(IMAPRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[IMAP]:

        stmt = select(IMAPModel)
        result = await self._session.execute(stmt)
        results = result.scalars().all()
        return [convert_imap_model_to_entity(res) for res in results]

    async def get_by_domain(self, domain: str) -> Optional[IMAP]:
        """
        Ищет запись, чей domain_pattern совпадает с переданным domain через SQL LIKE,
        сортирует по priority ASC и возвращает первую.
        """

        stmt = select(IMAPModel).where(IMAPModel.domain == domain).limit(1)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        if model:
            return convert_imap_model_to_entity(model)
        return None

    async def create(self, entity: IMAP) -> IMAP:

        model = convert_imap_entity_to_model(entity)
        self._session.add(model)
        await self._session.commit()
        return entity

    async def bulk_create(
        self,
        entities: list[IMAP],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[UUID] | None:
        if not entities:
            return []

        models = [convert_imap_entity_to_model(entity) for entity in entities]
        values = [model_to_dict(obj) for obj in models]
        stmt = insert(IMAPModel)

        if return_inserted_ids:
            stmt = stmt.returning(IMAPModel.id)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        result = await self._session.execute(stmt, values)
        await self._session.commit()

        if return_inserted_ids:
            return [row[0] for row in result.fetchall()]

    async def bulk_delete(
        self,
        ids: Optional[list[UUID]],
    ) -> int:

        stmt = delete(IMAPModel)
        if ids is not None:
            stmt = stmt.where(IMAPModel.id.in_(ids))

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount  # noqa
