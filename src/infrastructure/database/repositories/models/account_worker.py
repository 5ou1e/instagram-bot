import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime
from sqlalchemy import Enum as SaEnum
from sqlalchemy import ForeignKey, Index, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.working_group.entities.worker.work_state import AccountWorkerWorkState
from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class AccountWorkerModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "account_worker"

    working_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("working_group.id", ondelete="CASCADE")
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("account.id", ondelete="CASCADE")
    )
    proxy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("proxy.id", ondelete="SET NULL"), nullable=True
    )
    android_device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("android_device.id", ondelete="SET NULL"),
        nullable=True,
    )
    work_state: Mapped[AccountWorkerWorkState] = mapped_column(
        SaEnum(AccountWorkerWorkState, name="account_worker_work_state"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(Text, nullable=True)
    last_action_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    working_group = relationship(
        "WorkingGroupModel",
        back_populates="workers",
        overlaps="workers,working_groups",
    )
    account = relationship(
        "AccountModel",
        back_populates="worker",
        overlaps="workers,working_groups",
    )
    proxy = relationship("ProxyModel", backref="account_workers", lazy="joined")
    android_device = relationship(
        "AndroidDeviceModel",
        back_populates="workers",
        uselist=False,
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint(
            "working_group_id", "account_id", name="uq_account_working_group_pair"
        ),
        Index("idx_account_worker_work_state", "work_state"),
    )
