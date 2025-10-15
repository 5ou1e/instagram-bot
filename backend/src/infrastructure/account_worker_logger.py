import asyncio
import contextlib
import logging
from typing import List
from uuid import UUID

from uuid6 import uuid7

from src.domain.aggregates.account_worker.entities.account_worker_log import (
    AccountWorkerLog,
    AccountWorkerLogType,
    LogLevel,
)
from src.domain.aggregates.account_worker.repositories.account_worker_log import (
    AccountWorkerLogRepository,
)
from src.domain.shared.interfaces.logger import (
    AccountWorkerLogger,
    AccountWorkerLoggerFactory,
)
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.utils import current_datetime

logger = logging.getLogger(__name__)


class PostgresLogsWriter:
    """
    Обработчик, который «слушает» LOG_QUEUE и батчами записывает логи в БД.
    Нужно вызывать start() при старте, и shutdown() при остановке.
    """

    def __init__(
        self,
        uow: Uow,
        queue: asyncio.Queue,
        repository: AccountWorkerLogRepository,
        interval: float = 1.0,
        batch_size: int | None = None,
    ):
        self._uow = uow
        self._queue = queue
        self._repo = repository
        self._interval = interval
        self._batch_size = batch_size
        self._task: asyncio.Task | None = None
        self._running = False
        self._level = LogLevel.DEBUG

    def start(self, level: LogLevel = LogLevel.DEBUG) -> None:
        self._level = level
        """Запустить фоновую задачу"""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        while self._running:
            await asyncio.sleep(self._interval)
            await self._flush_batch()

    async def _flush_batch(self) -> None:
        batch: List[AccountWorkerLog] = []

        try:
            entry = self._queue.get_nowait()
            if entry.level.order >= self._level.order:
                batch.append(entry)

        except asyncio.QueueEmpty:
            return

        while (
            self._batch_size is None or len(batch) < self._batch_size
        ) and not self._queue.empty():
            entry = self._queue.get_nowait()
            if entry.level.order >= self._level.order:
                batch.append(entry)

        try:
            async with self._uow:
                await self._repo.bulk_create(batch, on_conflict_do_nothing=True)
        except Exception as e:
            logger.exception("Ошибка при записи батча логов в БД %s", e)
        finally:
            # пометить в очереди, что эти записи обработаны
            for _ in batch:
                self._queue.task_done()

    async def shutdown(self) -> None:
        self._running = False

        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

        while not self._queue.empty():
            await self._flush_batch()


class SeqNumber:
    def __init__(self):
        self.value = 0

    def increase(self):
        self.value += 1


class PostgresAccountWorkerLogger(AccountWorkerLogger):
    def __init__(
        self,
        account_id: UUID | None,
        queue: asyncio.Queue,
        logs_type: AccountWorkerLogType | None = None,
    ):
        self._account_id = account_id
        self._queue: asyncio.Queue[AccountWorkerLog] = queue
        self._logger = logging.getLogger(f"account.{account_id}")
        self._logs_type = logs_type or AccountWorkerLogType.DEFAULT
        self._seq_number = SeqNumber()

    def set_account_id(self, account_id: UUID) -> None:
        self._account_id = account_id

    async def _log(self, level: str, log_func, msg: str, *args, **kwargs):
        msg = str(msg)
        formatted = msg % args if args else msg
        log_func(f"[{self._account_id}] {formatted}")

        self._seq_number.increase()

        log = AccountWorkerLog(
            id=uuid7(),
            level=LogLevel(level),
            type=self._logs_type,
            message=formatted,
            account_id=self._account_id,
            created_at=current_datetime(),
            seq=self._seq_number.value,
        )

        try:
            self._queue.put_nowait(log)
        except asyncio.QueueFull:
            self._logger.warning("Ошибка при записи лога в очередь: %s", formatted)

    async def info(self, msg, *args, **kwargs):
        await self._log("INFO", self._logger.info, msg, *args, **kwargs)

    async def error(self, msg, *args, **kwargs):
        await self._log("ERROR", self._logger.error, msg, *args, **kwargs)

    async def debug(self, msg, *args, **kwargs):
        await self._log("DEBUG", self._logger.debug, msg, *args, **kwargs)

    async def warning(self, msg, *args, **kwargs):
        await self._log("WARNING", self._logger.warning, msg, *args, **kwargs)


class PostgresAccountWorkerLoggerFactory(AccountWorkerLoggerFactory):

    def __init__(self, queue: asyncio.Queue):
        self._queue: asyncio.Queue[AccountWorkerLog] = queue

    def create(self, account_id: UUID | None = None) -> AccountWorkerLogger:
        return PostgresAccountWorkerLogger(account_id, self._queue)
