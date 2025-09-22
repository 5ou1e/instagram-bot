import asyncio
import random
from uuid import UUID

from src.api.settings import config
from src.domain.account.repositories.account import AccountRepository
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
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


class AccountWorkerActionsWithUsersTaskExecutor(AccountWorkerTaskExecutor):

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

    async def execute(self, account_id: UUID, stop_event: asyncio.Event):
        with open(config.files.user_ids_for_follows_filepath, "r") as file:
            users_to_follow = [line.strip() for line in file]

        users_to_follow = users_to_follow[0:]

        async with self._uow:
            subtask = await self._account_worker_task_repository.get_by_id(
                self._subtask_id
            )
            account = await self._account_repository.get_by_id(account_id)
            working_group: WorkingGroup = (
                await self._working_group_repository.get_by_id(subtask.working_group_id)
            )

        working_group_config: WorkingGroupConfig = working_group.config

        for user_id in users_to_follow:
            if stop_event.is_set():
                return
            follow_flow = FollowUserFlow(
                ctx=FollowUserFlowContext(
                    uow=self._uow,
                    account_repository=self._account_repository,
                    logger=self._logger,
                    proxy_provider=self._proxy_provider,
                ),
                config=FollowUserFlowConfig(
                    instagram_network_config=working_group_config.instagram_network_config,
                ),
                authorization_flow=None,
            )

            await follow_flow.execute(account=account, user_id=str(user_id))

            await asyncio.sleep(random.randint(5, 15))
