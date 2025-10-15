from dataclasses import dataclass, field
from uuid import UUID

from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.services.account_worker.providers.proxy_provider import ProxyProvider
from src.domain.services.email_service import EmailService
from src.domain.services.worker_workflow.actions_old.instagram.auth.authorize_account import (
    AuthorizationFlow,
    AuthorizationFlowConfig,
    AuthorizationFlowContext,
)
from src.domain.services.worker_workflow.actions_old.instagram.unauthorized.reset_password_by_email import (
    ResetPasswordByEmailFlow,
)
from src.domain.shared.interfaces.logger import AccountWorkerLogger, Logger
from src.domain.shared.interfaces.uow import Uow


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
        self._worker_logger = logger

    def create_authorization_flow(
        self,
        config: AuthorizationFlowConfig,
        reset_password_flow: ResetPasswordByEmailFlow,
    ) -> AuthorizationFlow:
        return AuthorizationFlow(
            ctx=AuthorizationFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                logger=self._worker_logger,
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
                logger=self._worker_logger,
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            ),
            config=config,
        )


@dataclass
class Task:
    id: UUID
    name: str


@dataclass(kw_only=True)
class Workflow:
    id: UUID
    work_with_proxy: bool = True
    tasks: list[Task] = field(default_factory=list)


@dataclass
class WorkingGroup:
    id: UUID
    workflow: Workflow

    def change_workflow(self):
        pass


class ActionExecutorFactory:

    def __init__(
        self,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,
        proxy_provider: ProxyProvider,
        working_group_repository: WorkingGroupRepository,
        account_repository: AccountRepository,
        worker_logger: AccountWorkerLogger,
    ):
        self._uow = uow
        self._account_worker_repository = account_worker_repository
        self._working_group_repository = working_group_repository
        self._account_repository = account_repository
        self._proxy_provider = proxy_provider
        self._worker_logger = worker_logger

    def create_authorization_flow(
        self,
        config: AuthorizationFlowConfig,
    ) -> AuthorizationFlow:
        return AuthorizationFlow(
            ctx=AuthorizationFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                logger=self._worker_logger,
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            ),
            config=config,
            reset_password_flow=None,
        )
