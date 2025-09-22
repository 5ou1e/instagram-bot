import asyncio
import logging
from dataclasses import dataclass
from functools import partial
from typing import Any
from uuid import UUID

from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.entities.worker.work_state import AccountWorkerWorkState
from src.domain.working_group.exceptions import AccountWorkerIdDoesNotExistError
from src.domain.working_group.repositories.account_worker import AccountWorkerRepository
from src.domain.working_group.services.worker_workflow_executor import (
    AccountWorkerWorkflowExecutor,
)
from src.infrastructure.account_worker_logger import PostgresLogsWriter

logger = logging.getLogger(__name__)


@dataclass
class ExecutorInfo:
    executor_task: asyncio.Task[Any]
    stop_event: asyncio.Event
    pause_event: asyncio.Event


class WorkerWorkflowExecutorsManager:

    def __init__(self):
        from src.execution_service.settings.di.setup import (
            create_workers_manager_container,
        )

        self.container = create_workers_manager_container()
        self._executors: dict[UUID, ExecutorInfo] = {}
        self._logs_writer = None

    async def _create_executor_task(
        self,
        account_worker_id: UUID,
    ):
        stop_event = asyncio.Event()
        pause_event = asyncio.Event()

        async def _wrapper():
            async with self.container() as request_container:
                executor: AccountWorkerWorkflowExecutor = await request_container.get(
                    AccountWorkerWorkflowExecutor
                )

                await executor.execute(
                    account_worker_id,
                    stop_event=stop_event,
                )

        task = asyncio.create_task(_wrapper())

        task.add_done_callback(
            partial(
                self._on_executor_done_callback, account_worker_id=account_worker_id
            )
        )

        return ExecutorInfo(
            executor_task=task,
            stop_event=stop_event,
            pause_event=pause_event,
        )

    def _on_executor_done_callback(self, t: asyncio.Task, account_worker_id):
        self._executors.pop(account_worker_id, None)

        try:
            t.result()
        except asyncio.CancelledError:
            logger.info(
                "Флоу аккаунт-воркера %s отменен (cancelled)", account_worker_id
            )
        except Exception as e:
            logger.exception(
                "Возникло исключение во время исполнения флоу аккаунт-воркера %s | %s",
                account_worker_id,
                e,
            )

        asyncio.create_task(self._finish_worker(account_worker_id))

    async def _finish_worker(self, account_worker_id: UUID):
        """Переводим статус аккаунт-воркера в IDLE"""
        async with self.container() as request_container:
            uow: Uow = await request_container.get(Uow)
            account_worker_repository: AccountWorkerRepository = (
                await request_container.get(AccountWorkerRepository)
            )

            async with uow:
                account_worker = await account_worker_repository.acquire_by_id(
                    account_worker_id
                )
                if not account_worker:
                    raise AccountWorkerIdDoesNotExistError(
                        account_worker_id=account_worker_id
                    )

                # TODO пересмотреть этот момент
                if account_worker.work_state == AccountWorkerWorkState.WORKING:
                    account_worker.stop()

                account_worker.finish()

                await account_worker_repository.update(account_worker)

    async def _ensure_logs_writer_is_running(self):
        if not self._logs_writer:
            self._logs_writer = await self.container.get(PostgresLogsWriter)
            self._logs_writer.start()

    ### API ###
    async def start_worker(self, account_worker_id: UUID):

        await self._ensure_logs_writer_is_running()

        """ Запуск аккаунт-воркера """
        async with self.container() as request_container:
            uow: Uow = await request_container.get(Uow)
            account_worker_repository: AccountWorkerRepository = (
                await request_container.get(AccountWorkerRepository)
            )

            async with uow:
                account_worker = await account_worker_repository.acquire_by_id(
                    account_worker_id
                )
                if not account_worker:
                    raise AccountWorkerIdDoesNotExistError(
                        account_worker_id=account_worker_id
                    )

                account_worker.start()

                executor_info = self._executors.get(account_worker_id)
                if not executor_info:
                    self._executors[account_worker_id] = (
                        await self._create_executor_task(
                            account_worker_id,
                        )
                    )

                account_worker.work()

                await account_worker_repository.update(account_worker)

    async def stop_worker(self, account_worker_id: UUID):
        """Остановка аккаунт-воркера"""
        async with self.container() as request_container:
            uow: Uow = await request_container.get(Uow)
            account_worker_repository: AccountWorkerRepository = (
                await request_container.get(AccountWorkerRepository)
            )

            async with uow:
                account_worker = await account_worker_repository.acquire_by_id(
                    account_worker_id
                )
                if not account_worker:
                    raise AccountWorkerIdDoesNotExistError(
                        account_worker_id=account_worker_id
                    )

                account_worker.stop()

                executor_info = self._executors.get(account_worker_id)
                if executor_info:
                    executor_info.stop_event.set()
                else:
                    pass

                await account_worker_repository.update(account_worker)

    # async def _start_processes(self, count):
    #     logger.info(f"Запускаем {count} процессов обработки аккаунтов...")
    #
    #     for _ in range(count):
    #         stop_event = multiprocessing.Event()
    #
    #         commands_queue = multiprocessing.Queue()
    #
    #         p = multiprocessing.get_context("spawn").Process(
    #             target=spawn_worker,
    #             args=(
    #                 commands_queue,
    #                 stop_event,
    #             ),
    #         )
    #
    #         p.start()
    #
    #         self._processes.append(
    #             {
    #                 "process": p,
    #                 "commands_queue": commands_queue,
    #                 "stop_event": stop_event,
    #             }
    #         )
    #
    #     logger.info("Процессы обработки аккаунтов запущены")
    #
    # def start_account(self, worker_id: UUID):
    #     self._processes[0]["commands_queue"].put(
    #         WorkerWorkflowExecutorsSupervisorStartAccountCommand(
    #             worker_id=worker_id,
    #         ))
    #
    # def stop_account(self, worker_id: UUID):
    #     self._processes[0]["commands_queue"].put(
    #         WorkerWorkflowExecutorsSupervisorStopAccountCommand(
    #             worker_id=worker_id,
    #         ))
