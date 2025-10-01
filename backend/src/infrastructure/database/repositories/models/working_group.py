from sqlalchemy import JSON
from sqlalchemy import Enum as SaEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.working_group.entities.working_group.work_state import (
    WorkingGroupWorkState,
)
from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class WorkingGroupModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "working_group"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=True)
    work_state: Mapped[WorkingGroupWorkState] = mapped_column(
        SaEnum(WorkingGroupWorkState), nullable=False
    )

    workers = relationship(
        "AccountWorkerModel",
        back_populates="working_group",
        cascade="all, delete-orphan",
        overlaps="workers,working_groups",
        lazy="noload",
    )

    worker_tasks = relationship(
        "AccountWorkerTaskModel",
        back_populates="working_group",
        lazy="noload",
    )
