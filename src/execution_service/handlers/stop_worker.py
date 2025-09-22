from dataclasses import dataclass
from uuid import UUID

from src.execution_service.services.worker_workflow_executors_manager import (
    WorkerWorkflowExecutorsManager,
)


@dataclass(kw_only=True, slots=True)
class StopWorkersCommand:
    worker_ids: list[UUID]


class StopWorkersCommandHandler:

    def __init__(
        self,
        workers_manager: WorkerWorkflowExecutorsManager,
    ):
        self._workers_manager = workers_manager

    async def __call__(self, command: StopWorkersCommand):
        for worker_id in command.worker_ids:
            await self._workers_manager.stop_worker(account_worker_id=worker_id)
