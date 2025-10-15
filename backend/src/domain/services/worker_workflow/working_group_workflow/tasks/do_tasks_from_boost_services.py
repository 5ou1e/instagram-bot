import asyncio
import random
from uuid import UUID

from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker

from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.aggregates.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.aggregates.working_group.entities.working_group.entity import (
    WorkingGroup,
)
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.services.worker_workflow.actions_old.instagram.authorized.extra_requests import \
    SendExtraRequestsFlowConfig, SendExtraRequestsFlow, SendExtraRequestsFlowContext
from src.domain.services.worker_workflow.actions_old.instagram.authorized.follow_user import (
    FollowUserFlow,
    FollowUserFlowConfig,
    FollowUserFlowContext,
)
from src.domain.services.worker_workflow.providers.proxy_provider import ProxyProvider
from src.domain.services.worker_workflow.working_group_workflow.tasks.base import (
    AccountWorkerTaskExecutor,
)
from src.domain.shared.interfaces.boost_services.exceptions import VenroNoTasks
from src.domain.shared.interfaces.instagram.exceptions import (
    UserIdNotFound,
    UserNotFoundError,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.infrastructure.boost_services.venro_client import VenroClientImpl


class AccountWorkerDoTasksFromBoostServicesTaskExecutor(AccountWorkerTaskExecutor):

    def __init__(
        self,
        task_id: UUID,
        uow: Uow,
        account_repository: AccountRepository,
        account_worker_repository: AccountWorkerRepository,
        proxy_provider: ProxyProvider,
        working_group_repository: WorkingGroupRepository,
        logger: Logger,
    ):
        self._uow = uow
        self._task_id = task_id
        self._proxy_provider = proxy_provider
        self._account_repository = account_repository
        self._account_worker_repository = account_worker_repository
        self._working_group_repository = working_group_repository
        self._worker_logger = logger

    async def execute(self, worker: AccountWorker, stop_event: asyncio.Event):

        async with self._uow:
            account = await self._account_repository.get_by_id(worker.account_id)
            working_group: WorkingGroup = (
                await self._working_group_repository.get_by_id(worker.working_group_id)
            )

        working_group_config: WorkingGroupConfig = working_group.config

        venro_client = VenroClientImpl()

        api_key = "494dc3b6d5c6e371afc15ea93aca6ef3"

        if not account.user_id:
            raise ValueError(f"У аккаунта нету user-id")

        bot_id = account.user_id
        service_id = 1

        TOTAL_COMPLETED_COUNT = 50
        completed_count = 0

        while True:
            if completed_count >= TOTAL_COMPLETED_COUNT:
                return
            if stop_event.is_set():
                return

            if completed_count >= 50:
                await self._send_extra_requests(worker, working_group_config)

            try:
                await self._worker_logger.info(f"Получаю задание с Venro...")
                venro_task = await venro_client.get_task_follow(
                    api_key,
                    bot_id,
                    service_id,
                )
                await self._worker_logger.info(f"Получил задание")
            except VenroNoTasks as e:
                await self._worker_logger.info(f"Нету заданий на Venro")
                await asyncio.sleep(10)
                continue
            except Exception as e:
                await self._worker_logger.error(
                    f"Не удалось получить задание с Venro: {e}"
                )
                raise

            follow_flow = FollowUserFlow(
                ctx=FollowUserFlowContext(
                    uow=self._uow,
                    account_repository=self._account_repository,
                    logger=self._worker_logger,
                    proxy_provider=self._proxy_provider,
                    account_worker_repository=self._account_worker_repository,
                ),
                config=FollowUserFlowConfig(
                    instagram_network_config=working_group_config.instagram_network_config,
                ),
                authorization_flow=None,
            )

            user_id = venro_task.item_id

            try:
                await follow_flow.execute(worker=worker, user_id=str(user_id))
            except (UserNotFoundError, UserIdNotFound) as e:
                continue

            try:
                await self._worker_logger.info(
                    f"Отправляю задание на проверку Venro ..."
                )
                await venro_client.send_task_done(
                    api_key,
                    venro_task.id,
                    account.user_id,
                    account.username,
                )
                await self._worker_logger.error(f"Отправил задание на проверку")
            except Exception as e:
                await self._worker_logger.error(
                    f"Не удалось отправить результат выполнения задания на Venro: {e}"
                )
                raise

            completed_count += 1
            await asyncio.sleep(random.randint(5, 15))

    async def _send_extra_requests(self, worker, working_group_config):
        flow = SendExtraRequestsFlow(
            ctx=SendExtraRequestsFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                logger=self._worker_logger,
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            ),
            config=SendExtraRequestsFlowConfig(
                instagram_network_config=working_group_config.instagram_network_config,
            ),
            authorization_flow=None,
        )
        await flow.execute(worker)
