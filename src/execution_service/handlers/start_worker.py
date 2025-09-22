import logging
from dataclasses import dataclass
from uuid import UUID

from src.execution_service.services.worker_workflow_executors_manager import (
    WorkerWorkflowExecutorsManager,
)

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class StartWorkersCommand:
    worker_ids: list[UUID]


class StartWorkersCommandHandler:

    def __init__(
        self,
        workers_manager: WorkerWorkflowExecutorsManager,
    ):
        self._workers_manager = workers_manager

    async def __call__(self, command: StartWorkersCommand):
        for worker_id in command.worker_ids:
            await self._workers_manager.start_worker(account_worker_id=worker_id)
