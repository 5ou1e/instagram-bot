import asyncio
import logging
import traceback
from uuid import UUID

from src.domain.shared.exceptions import DomainError
from src.domain.shared.interfaces.logger import AccountWorkerLogger
from src.domain.shared.interfaces.uow import Uow
from src.domain.account_worker.repositories.account_worker import AccountWorkerRepository
from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.domain.account_worker.services.working_group_workflow.tasks.executor_factory import (
    AccountWorkerTaskExecutorFactory,
)
from src.domain.account_worker.services.working_group_workflow.worker_prepare_service import (
    AccountWorkerPrepareBeforeWorkService,
)

logger = logging.getLogger(__name__)


class AccountWorkerWorkflowExecutor:
    """Выполняет последовательность задач аккаунт-воркера настроенных в рабочей группе"""

    def __init__(
        self,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,
        working_group_repository: WorkingGroupRepository,
        worker_logger: AccountWorkerLogger,
        worker_prepare_service: AccountWorkerPrepareBeforeWorkService,
        account_worker_task_executor_factory: AccountWorkerTaskExecutorFactory,
    ):
        self._uow = uow
        self._account_worker_repository = account_worker_repository
        self._account_worker_task_executor_factory = account_worker_task_executor_factory
        self._worker_prepare_service = worker_prepare_service
        self._working_group_repository = working_group_repository
        self._worker_logger = worker_logger

    async def execute(
        self,
        worker_id: UUID,
        stop_event: asyncio.Event,
    ) -> None:
        try:
            async with self._uow:
                worker = await self._account_worker_repository.acquire_by_id(worker_id)

                self._worker_logger.set_account_id(worker.account_id)

                working_group = await self._working_group_repository.get_by_id(
                    worker.working_group_id
                )
                tasks = working_group.get_enabled_worker_tasks()

            await self._worker_prepare_service.prepare(worker)

            await self._worker_logger.info("Начал работу")

            for task in tasks:
                task_executor = self._account_worker_task_executor_factory.create(task)
                await task_executor.execute(
                    worker=worker,
                    stop_event=stop_event,
                )

        except Exception as e:
            if isinstance(e, DomainError):
                pass
            else:
                tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                await self._worker_logger.error(tb)
            raise e
        finally:
            async with self._uow:
                worker = await self._account_worker_repository.acquire_by_id(worker_id)
                worker.change_status("Не работаю")
                await self._account_worker_repository.update(worker)
