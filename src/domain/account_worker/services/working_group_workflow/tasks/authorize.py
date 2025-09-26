import asyncio
from uuid import UUID

from src.domain.account.repositories.account import AccountRepository
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.services.email_service import EmailService
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.working_group.entities.working_group.entity import WorkingGroup
from src.domain.account_worker.repositories.account_worker import AccountWorkerRepository

from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.domain.account_worker.services.flows.auth.authorize_account import (
    AuthorizationFlow,
    AuthorizationFlowConfig,
    AuthorizationFlowContext,
)
from src.domain.account_worker.services.flows.unauthorized.reset_password_by_email import (
    ResetPasswordByEmailFlow,
    ResetPasswordByEmailFlowConfig,
    ResetPasswordByEmailFlowContext,
)
from src.domain.account_worker.services.providers.proxy_provider import ProxyProvider
from src.domain.account_worker.services.working_group_workflow.tasks.base import (
    AccountWorkerTaskExecutor,
)


class AccountWorkerAuthorizeAccountTaskExecutor(AccountWorkerTaskExecutor):

    def __init__(
        self,
        task_id: UUID,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,

        proxy_provider: ProxyProvider,
        working_group_repository: WorkingGroupRepository,
        account_repository: AccountRepository,
        logger: Logger,
        email_service: EmailService,
    ):
        self._task_id = task_id
        self._uow = uow
        self._proxy_provider = proxy_provider
        self._account_worker_repository = account_worker_repository
        self._working_group_repository = working_group_repository
        self._account_repository = account_repository
        self._logger = logger
        self._email_service = email_service

    async def execute(self, worker: AccountWorker, stop_event: asyncio.Event):
        # TODO реворк, тут нужен синглтон с кешом провайдящий обьект задачи

        async with self._uow:
            working_group: WorkingGroup = await self._working_group_repository.get_by_id(
                worker.working_group_id
            )

        working_group_config: WorkingGroupConfig = working_group.config

        reset_password_flow = ResetPasswordByEmailFlow(
            ctx=ResetPasswordByEmailFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                email_service=self._email_service,
                logger=self._logger,
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            ),
            config=ResetPasswordByEmailFlowConfig(
                instagram_network_config=working_group_config.instagram_network_config,
            ),
        )

        authorization_flow = AuthorizationFlow(
            ctx=AuthorizationFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                logger=self._logger,
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            ),
            config=AuthorizationFlowConfig(
                instagram_network_config=working_group_config.instagram_network_config,
            ),
            reset_password_flow=reset_password_flow,
        )

        await authorization_flow.execute(worker)


class FlowExecutorFactory:
    # TODO допилить эту штуку

    def __init__(
        self,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,
        proxy_provider: ProxyProvider,
        working_group_repository: WorkingGroupRepository,
        account_repository: AccountRepository,
        logger: Logger,
        email_service: EmailService,
    ):
        self._uow = uow
        self._account_worker_repository = account_worker_repository
        self._working_group_repository = working_group_repository
        self._account_repository = account_repository
        self._email_service = email_service
        self._proxy_provider = proxy_provider
        self._logger = logger

    def create_authorization_flow(
        self,
        config: AuthorizationFlowConfig,
        reset_password_flow: ResetPasswordByEmailFlow,
    ) -> AuthorizationFlow:
        return AuthorizationFlow(
            ctx=AuthorizationFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                logger=self._logger,
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            ),
            config=config,
            reset_password_flow=reset_password_flow,
        )

    def create_reset_password_flow(
        self,
        config: ResetPasswordByEmailFlowConfig,
    ) -> ResetPasswordByEmailFlow:
        return ResetPasswordByEmailFlow(
            ctx=ResetPasswordByEmailFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                email_service=self._email_service,
                logger=self._logger,
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            ),
            config=config,
        )
