from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.aggregates.working_group.entities.working_group.work_state import (
    WorkingGroupWorkState,
)


@dataclass(kw_only=True, slots=True)
class WorkingGroupDTO:
    id: UUID
    work_state: WorkingGroupWorkState
    name: str | None = None
    config: dict = field(default_factory=dict)
    worker_tasks: list = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    working_workers_count: int = 0
    starting_workers_count: int = 0
    stopping_workers_count: int = 0
    idle_workers_count: int = 0


@dataclass(kw_only=True, slots=True)
class WorkingGroupsDTO:
    working_groups: list[WorkingGroupDTO]
