import asyncio
import random
from uuid import UUID

from src.domain.account.repositories.account import AccountRepository
from src.domain.shared.interfaces.boost_services.exceptions import VenroNoTasks
from src.domain.shared.interfaces.instagram.exceptions import (
    UserIdNotFound,
    UserNotFoundError,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.working_group.entities.worker.entity import AccountWorker
from src.domain.working_group.entities.working_group.entity import WorkingGroup
from src.domain.working_group.repositories.account_worker_task import (
    AccountWorkerTaskRepository,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.domain.working_group.services.flows.authorized.follow_user_flow import (
    FollowUserFlow,
    FollowUserFlowConfig,
    FollowUserFlowContext,
)
from src.domain.working_group.services.providers.proxy_provider import ProxyProvider
from src.domain.working_group.services.task_executors.base import (
    AccountWorkerTaskExecutor,
)
from src.infrastructure.boost_services.venro_client import VenroClientImpl


class AccountWorkerDoTasksFromBoostServicesTaskExecutor(AccountWorkerTaskExecutor):

    def __init__(
        self,
        subtask_id: UUID,
        uow: Uow,
        account_repository: AccountRepository,
        proxy_provider: ProxyProvider,
        account_worker_task_repository: AccountWorkerTaskRepository,
        working_group_repository: WorkingGroupRepository,
        logger: Logger,
    ):
        self._uow = uow
        self._subtask_id = subtask_id
        self._proxy_provider = proxy_provider
        self._account_repository = account_repository
        self._working_group_repository = working_group_repository
        self._account_worker_task_repository = account_worker_task_repository
        self._logger = logger

    async def execute(self, worker: AccountWorker, stop_event: asyncio.Event):

        async with self._uow:
            subtask = await self._account_worker_task_repository.get_by_id(
                self._subtask_id
            )
            account = await self._account_repository.get_by_id(worker.account_id)
            task: WorkingGroup = await self._working_group_repository.get_by_id(
                subtask.working_group_id
            )

        task_config: WorkingGroupConfig = task.config

        venro_client = VenroClientImpl()

        api_key = "494dc3b6d5c6e371afc15ea93aca6ef3"
        bot_id = account.user_id
        service_id = 1

        completed_count = 0

        while completed_count <= 50:
            if stop_event.is_set():
                return
            try:
                await self._logger.error(f"Получаю задание с Venro...")
                venro_task = await venro_client.get_task_follow(
                    api_key,
                    bot_id,
                    service_id,
                )
                await self._logger.error(f"Получил задание")
            except VenroNoTasks as e:
                await self._logger.error(f"Нету заданий на Venro")
                await asyncio.sleep(10)
                continue
            except Exception as e:
                await self._logger.error(f"Не удалось получить задание с Venro: {e}")
                raise

            follow_flow = FollowUserFlow(
                ctx=FollowUserFlowContext(
                    uow=self._uow,
                    account_repository=self._account_repository,
                    logger=self._logger,
                    proxy_provider=self._proxy_provider,
                ),
                config=FollowUserFlowConfig(
                    instagram_network_config=task_config.instagram_network_config,
                ),
                authorization_flow=None,
            )

            user_id = venro_task.item_id

            try:
                await follow_flow.execute(worker=worker, user_id=str(user_id))
            except (UserNotFoundError, UserIdNotFound) as e:
                continue

            try:
                await self._logger.error(f"Отправляю задание на проверку Venro ...")
                await venro_client.send_task_done(
                    api_key,
                    venro_task.id,
                    account.user_id,
                    account.username,
                )
                await self._logger.error(f"Отправил задание на проверку")
            except Exception as e:
                await self._logger.error(
                    f"Не удалось отправить результат выполнения задания на Venro: {e}"
                )
                raise

            completed_count += 1
            await asyncio.sleep(random.randint(5, 15))
