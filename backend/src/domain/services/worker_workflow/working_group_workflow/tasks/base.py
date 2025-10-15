import asyncio
from abc import ABC, abstractmethod

from src.domain.aggregates.account_worker.entities.account_worker.entity import (
    AccountWorker,
)


class AccountWorkerTaskExecutor(ABC):
    """Абстрактный базовый класс - Исполнитель задачи воркера"""

    @abstractmethod
    async def execute(
        self, worker: AccountWorker, stop_event: asyncio.Event
    ) -> None: ...
