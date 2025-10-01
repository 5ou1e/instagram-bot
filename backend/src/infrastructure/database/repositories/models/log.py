import uuid

from sqlalchemy import UUID
from sqlalchemy import Enum as SaEnum
from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.account_worker.entities.account_worker_log import LogLevel
from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class AccountWorkerLogModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "account_worker_log"

    level: Mapped[LogLevel] = mapped_column(
        SaEnum(LogLevel),
        nullable=False,
        name="log_level"
    )
    type: Mapped[str] = mapped_column(String(25), nullable=False)
    seq: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=True,
    )

    account = relationship("AccountModel", backref="logs")

    __table_args__ = (
        Index("idx_logs_account_created_seq", "account_id", "created_at", "seq"),
    )
