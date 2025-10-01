import asyncio
from datetime import datetime
from uuid import UUID

from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.utils import current_datetime
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository


class WorkingGroupConfigProvider:
    """Провайдер конфигурации рабочей группы с авто-обновлением каждые interval секунд."""

    def __init__(
        self,
        working_group_id: UUID,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
        refresh_interval: float = 1.0,  # секунды
    ):
        self._working_group_id = working_group_id
        self._uow = uow
        self._working_group_repository = working_group_repository
        self._refresh_interval = refresh_interval

        self._cached_config: WorkingGroupConfig | None = None
        self._last_fetched: datetime | None = None
        self._lock = asyncio.Lock()

    async def provide_config(self) -> WorkingGroupConfig:
        async with self._lock:
            now = current_datetime()
            if (
                self._cached_config is None
                or self._last_fetched is None
                or (now - self._last_fetched).total_seconds() >= self._refresh_interval
            ):
                async with self._uow:
                    working_group = await self._working_group_repository.get_by_id(
                        self._working_group_id
                    )
                    self._cached_config = working_group.config
                    self._last_fetched = now
            return self._cached_config
