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

from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.domain.account_worker.services.flows.authorized.follow_user import (
    FollowUserFlow,
    FollowUserFlowConfig,
    FollowUserFlowContext,
)
from src.domain.account_worker.services.providers.proxy_provider import ProxyProvider
from src.domain.account_worker.services.working_group_workflow.tasks.base import (
    AccountWorkerTaskExecutor,
)


class AccountWorkerActionsWithUsersTaskExecutor(AccountWorkerTaskExecutor):

    def __init__(
        self,
        task_id: UUID,
        uow: Uow,
        account_repository: AccountRepository,
        proxy_provider: ProxyProvider,

        working_group_repository: WorkingGroupRepository,
        logger: Logger,
    ):
        self._uow = uow
        self._task_id = task_id
        self._proxy_provider = proxy_provider
        self._account_repository = account_repository
        self._working_group_repository = working_group_repository
        self._logger = logger

    async def execute(self, account_id: UUID, stop_event: asyncio.Event):
        with open(config.files.user_ids_for_follows_filepath, "r") as file:
            users_to_follow = [line.strip() for line in file]

        users_to_follow = users_to_follow[0:]

        async with self._uow:
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
