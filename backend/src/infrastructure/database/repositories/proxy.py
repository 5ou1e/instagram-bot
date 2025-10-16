import random
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, func, select, tuple_, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dtos.pagination import Pagination, PaginationResult
from src.application.common.interfaces.proxies_reader import ProxiesReader
from src.application.features.proxy.dto import ProxiesDTO, ProxyDTO
from src.domain.aggregates.proxy.entities import Proxy, ProxyProtocol
from src.domain.aggregates.proxy.repository import ProxyRepository
from src.infrastructure.database.repositories.models.common import model_to_dict
from src.infrastructure.database.repositories.models.proxy import ProxyModel


def convert_proxy_entity_to_model(entity: Proxy) -> ProxyModel:
    return ProxyModel(
        id=entity.id,
        protocol=entity.protocol,
        host=entity.host,
        port=entity.port,
        username=entity.username,
        password=entity.password,
        usage=entity.usage,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def convert_proxy_model_to_entity(model: ProxyModel) -> Proxy:
    return Proxy(
        id=model.id,
        protocol=ProxyProtocol(model.protocol),
        host=model.host,
        port=model.port,
        username=model.username,
        password=model.password,
        usage=model.usage,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class PostgresProxyRepository(ProxyRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_random(self) -> Proxy | None:
        stmt = select(ProxyModel)
        result = await self._session.execute(stmt)
        proxies = result.scalars().all()
        if not proxies:
            return None
        return convert_proxy_model_to_entity(random.choice(proxies))

    async def get_all(self) -> list[Proxy]:
        stmt = select(ProxyModel)
        result = await self._session.execute(stmt)
        results = result.scalars().all()
        return [convert_proxy_model_to_entity(res) for res in results]

    async def create(self, entity: Proxy) -> Proxy:
        model = convert_proxy_entity_to_model(entity)
        self._session.add(model)

        return entity

    async def bulk_create(
        self,
        entities: list[Proxy],
        on_conflict_do_nothing: bool = False,
    ) -> list[Proxy] | None:
        if not entities:
            return []

        models = [convert_proxy_entity_to_model(account) for account in entities]
        values = [model_to_dict(m) for m in models]

        stmt = insert(ProxyModel).values(values)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        stmt = stmt.returning(ProxyModel)

        result = await self._session.execute(stmt)
        created_models = result.scalars().all()

        for account, model in zip(entities, created_models):
            account.id = model.id

        return entities

    async def bulk_delete(
        self,
        ids: Optional[list[UUID]],
    ) -> int:

        stmt = delete(ProxyModel)  # Удалить все записи
        if ids is not None:
            stmt = stmt.where(ProxyModel.id.in_(ids))

        result = await self._session.execute(stmt)
        return result.rowcount  # noqa

    async def acquire_least_used(self) -> Proxy | None:
        # 1. Получаем минимальный usage
        usage_stmt = select(func.min(ProxyModel.usage))
        result = await self._session.execute(usage_stmt)
        min_usage = result.scalar()

        if min_usage is None:
            return None

        # 2. Выбираем случайную прокси с этим usage и блокируем
        stmt = (
            select(ProxyModel)
            .where(ProxyModel.usage == min_usage)
            .order_by(func.random())  # PostgreSQL
            .limit(1)
            .with_for_update(skip_locked=True)
        )

        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            return convert_proxy_model_to_entity(model)
        return None

    async def update(self, entity: Proxy) -> None:
        model = convert_proxy_entity_to_model(entity)
        await self._session.merge(model)

    async def get_by_unique_keys(self, unique_keys: list[tuple]) -> list[Proxy]:
        if not unique_keys:
            return []

        stmt = select(ProxyModel).where(
            tuple_(
                ProxyModel.protocol,
                ProxyModel.host,
                ProxyModel.port,
                ProxyModel.username,
                ProxyModel.password,
            ).in_(unique_keys)
        )

        result = await self._session.execute(stmt)
        return [convert_proxy_model_to_entity(m) for m in result.scalars().all()]


class PostgresProxiesReader(ProxiesReader):
    """Читает прокси из таблицы proxy и возвращает DTO."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_proxies(
        self,
        pagination: Pagination,
    ) -> ProxiesDTO:
        limit, offset = pagination.limit_offset

        # 1) Общее количество
        count_stmt = text("SELECT COUNT(*) FROM proxy")
        total_count_result = await self._session.execute(count_stmt)
        total_count = int(total_count_result.scalar_one())

        select_stmt = text(
            """
            SELECT
                p.id,
                p.protocol,
                p.host,
                p.port,
                p.username,
                p.password,
                p.created_at
            FROM proxy p
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT :limit OFFSET :offset
            """
        )

        result = await self._session.execute(
            select_stmt,
            {"limit": limit, "offset": offset},
        )
        rows = result.all()

        proxies = [self._to_proxy_dto(r) for r in rows]

        return ProxiesDTO(
            proxies=proxies,
            pagination=PaginationResult.from_pagination(
                pagination=pagination,
                count=len(proxies),
                total_count=total_count,
            ),
        )

    @staticmethod
    def _to_proxy_dto(row) -> ProxyDTO:
        return ProxyDTO(
            id=row.id,
            protocol=row.protocol,
            host=row.host,
            port=int(row.port),
            username=row.username or "",
            password=row.password or "",
            created_at=row.created_at,
        )

