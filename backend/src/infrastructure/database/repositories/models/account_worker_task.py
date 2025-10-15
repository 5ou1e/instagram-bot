import uuid

from sqlalchemy import JSON, UUID, Boolean
from sqlalchemy import Enum as SaEnum
from sqlalchemy import ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.aggregates.working_group.entities.worker_task.base import (
    AccountWorkerTaskType,
)
from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class AccountWorkerTaskModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "account_worker_task"

    type: Mapped[AccountWorkerTaskType] = mapped_column(
        SaEnum(
            AccountWorkerTaskType,
            name="account_worker_task_type_enum",
        ),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=True)

    working_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("working_group.id", ondelete="CASCADE"),
        nullable=False,
    )

    working_group = relationship(
        "WorkingGroupModel",
        back_populates="worker_tasks",
    )
