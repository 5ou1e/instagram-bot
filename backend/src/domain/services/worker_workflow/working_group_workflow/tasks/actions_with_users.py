import asyncio
import random
from uuid import UUID

from src.api.settings import config
from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.aggregates.working_group.entities.working_group.entity import (
    WorkingGroup,
)
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.services.worker_workflow.actions_old.instagram.authorized.follow_user import (
    FollowUserFlow,
    FollowUserFlowConfig,
    FollowUserFlowContext,
)
from src.domain.services.worker_workflow.providers.proxy_provider import ProxyProvider
from src.domain.services.worker_workflow.working_group_workflow.tasks.base import (
    AccountWorkerTaskExecutor,
)
from src.domain.shared.interfaces.logger import AccountWorkerLogger
from src.domain.shared.interfaces.uow import Uow


class AccountWorkerActionsWithUsersTaskExecutor(AccountWorkerTaskExecutor):

    def __init__(
        self,
        task_id: UUID,
        uow: Uow,
        account_repository: AccountRepository,
        proxy_provider: ProxyProvider,
        working_group_repository: WorkingGroupRepository,
        logger: AccountWorkerLogger,
    ):
        self._uow = uow
        self._task_id = task_id
        self._proxy_provider = proxy_provider
        self._account_repository = account_repository
        self._working_group_repository = working_group_repository
        self._worker_logger = logger

    async def execute(self, account_id: UUID, stop_event: asyncio.Event):
        # TODO Refactor
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
                    logger=self._worker_logger,
                    proxy_provider=self._proxy_provider,
                ),
                config=FollowUserFlowConfig(
                    instagram_network_config=working_group_config.instagram_network_config,
                ),
                authorization_flow=None,
            )

            await follow_flow.execute(account=account, user_id=str(user_id))

            await asyncio.sleep(random.randint(5, 15))
