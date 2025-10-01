import uuid
from datetime import datetime


from sqlalchemy import JSON, BigInteger, DateTime, Index, String, text, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class AccountModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "account"

    username: Mapped[str] = mapped_column(String(90), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    email_username: Mapped[str] = mapped_column(String(255), nullable=True)
    email_password: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

    password_changed_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    action_statistics: Mapped[dict] = mapped_column(
        JSON, nullable=False, server_default=text("'{}'::jsonb")
    )

    worker = relationship(
        "AccountWorkerModel",
        back_populates="account",
        uselist=False,  # один аккаунт = одна рабочая группа
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (Index("idx_username", "username"),)
