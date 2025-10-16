from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from uuid6 import UUID

from src.domain.aggregates.account.entities.account import (
    Account,
    AccountActionStatistics,
)
from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account.value_objects import Email
from src.infrastructure.database.repositories.models import AccountWorkerModel
from src.infrastructure.database.repositories.models.account import (
    AccountModel as AccountModel,
)
from src.infrastructure.database.repositories.models.common import model_to_dict


def convert_account_model_to_entity(model: AccountModel) -> Account:
    return Account(
        id=model.id,
        username=model.username,
        password=model.password,
        user_id=model.user_id,
        comment=model.comment,
        email=Email(
            username=model.email_username,
            password=model.email_password,
        ),
        action_statistics=AccountActionStatistics.from_dict(model.action_statistics),
        password_changed_datetime=model.password_changed_datetime,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def convert_account_entity_to_model(entity: Account) -> AccountModel:
    return AccountModel(
        id=entity.id,
        username=entity.username,
        password=entity.password,
        user_id=entity.user_id,
        comment=entity.comment,
        email_username=entity.email.username if entity.email is not None else None,
        email_password=entity.email.password if entity.email is not None else None,
        action_statistics=entity.action_statistics.to_dict(),
        password_changed_datetime=entity.password_changed_datetime,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


class PostgresAccountRepository(AccountRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def acquire_by_id(self, id: UUID, skip_locked=False) -> Account | None:
        ta_alias = aliased(AccountWorkerModel)

        stmt = (
            select(AccountModel)
            .where(AccountModel.id == id)
            .with_for_update(
                of=AccountModel, skip_locked=skip_locked
            )  # блокируем только AccountModel
        )

        stmt_ta = (
            select(AccountWorkerModel)
            .where(AccountWorkerModel.account_id == id)
            .with_for_update(skip_locked=skip_locked)
        )
        result_ta = await self._session.execute(stmt_ta)

        result = await self._session.execute(stmt)

        model = result.unique().scalar_one_or_none()
        return convert_account_model_to_entity(model) if model else None

    async def acquire_all(self, skip_locked: bool = False) -> list[Account]:
        stmt = select(AccountModel).with_for_update(
            of=AccountModel,
            skip_locked=skip_locked,
        )
        result = await self._session.execute(stmt)
        models = result.unique().scalars().all()

        return [convert_account_model_to_entity(m) for m in models]

    async def acquire_by_ids(
        self,
        ids: list[UUID],
        skip_locked: bool = False
    ) -> list[Account]:
        if not ids:
            return []

        stmt = (
            select(AccountModel)
            .where(AccountModel.id.in_(ids))
            .with_for_update(
                of=AccountModel,
                skip_locked=skip_locked,
            )
        )

        result = await self._session.execute(stmt)
        models = result.unique().scalars().all()

        return [convert_account_model_to_entity(m) for m in models]

    async def get_by_id(self, account_id: UUID) -> Account | None:
        result = await self._session.execute(
            select(AccountModel).where(AccountModel.id == account_id)
        )
        instance = result.unique().scalar_one_or_none()
        if instance:
            return convert_account_model_to_entity(instance)
        return None

    async def get_one(self) -> Account | None:
        result = await self._session.execute(select(AccountModel).limit(1))
        instance = result.unique().scalar_one_or_none()
        if instance:
            return convert_account_model_to_entity(instance)
        return None

    async def get(self, ids: Optional[list[UUID]] = None) -> list[Account]:
        stmt = select(AccountModel)
        if ids is not None:
            stmt = stmt.where(AccountModel.id.in_(ids))

        result = await self._session.execute(stmt)
        models = result.unique().scalars().all()

        return [convert_account_model_to_entity(model) for model in models]

    async def get_all(self) -> list[Account]:
        result = await self._session.execute(select(AccountModel))
        rows = result.unique().scalars().all()
        return [convert_account_model_to_entity(row) for row in rows]

    async def create(self, account: Account) -> Account:
        raise NotImplementedError

    async def update(self, account: Account) -> None:
        "Обновляем обьект в БД"

        model = convert_account_entity_to_model(account)
        await self._session.merge(model)

    async def bulk_delete(
        self,
        ids: Optional[list[UUID]],
    ) -> int:
        stmt = delete(AccountModel)  # Удалить все записи
        if ids is not None:
            stmt = stmt.where(AccountModel.id.in_(ids))

        result = await self._session.execute(stmt)
        return result.rowcount

    async def bulk_create(
        self,
        entities: list[Account],
        on_conflict_do_nothing: bool = False,
        return_inserted_ids: bool = False,
    ) -> list[Account] | None:
        """Create workers and return them with DB-generated ids"""
        if not entities:
            return []

        models = [convert_account_entity_to_model(account) for account in entities]
        values = [model_to_dict(m) for m in models]

        stmt = insert(AccountModel).values(values)

        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing()

        stmt = stmt.returning(AccountModel)

        result = await self._session.execute(stmt)
        created_models = result.unique().scalars().all()

        # Обновляем id в исходных объектах
        for account, model in zip(entities, created_models):
            account.id = model.id
        await self._session.commit()

        return entities

    async def get_by_usernames(self, usernames: list[str]) -> list[Account]:
        if not usernames:
            return []

        stmt = select(AccountModel).where(AccountModel.username.in_(usernames))
        result = await self._session.execute(stmt)
        rows = result.unique().scalars().all()
        return [convert_account_model_to_entity(row) for row in rows]

    async def get_existing_usernames(self, usernames: list[str] = None) -> list[str]:
        stmt = select(AccountModel.username).where(AccountModel.username.in_(usernames))
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        return rows  # noqa
