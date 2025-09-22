import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, Integer, func, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid6 import uuid7


# declarative base class
class Base(DeclarativeBase):
    pass


class IntIDMixin:
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, sort_order=-1000
    )


class UUIDIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
        sort_order=-1000,
    )


class TimestampsMixin:
    """Базовый класс для моделей с временными метками"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), sort_order=-1
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        sort_order=-1,
    )


def model_to_dict(obj) -> dict:
    """
    Конвертирует SQLAlchemy ORM-объект в dict по его колонкам.
    """
    return {
        column.key: getattr(obj, column.key) for column in inspect(obj).mapper.columns
    }
