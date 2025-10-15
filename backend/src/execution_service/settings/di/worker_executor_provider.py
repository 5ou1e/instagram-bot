import asyncio
from typing import AsyncIterable

from dishka import Provider, Scope, WithParents, from_context, provide, provide_all
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account_worker.entities.account_worker_log.account_worker.entity import (
    AccountWorkerID,
)
from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.aggregates.android_device_hardware.repositories.android_device_hardware import (
    AndroidDeviceHardwareRepository,
)
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.services.email_service import EmailServiceFactory
from src.domain.services.worker_workflow.providers.proxy_provider import ProxyProvider
from src.domain.services.worker_workflow.working_group_workflow.tasks.executor_factory import (
    AccountWorkerTaskExecutorFactory,
)
from src.domain.services.worker_workflow.working_group_workflow.worker_prepare_service import (
    AccountWorkerPrepareBeforeWorkService,
)
from src.domain.services.worker_workflow.working_group_workflow.worker_workflow_executor import (
    AccountWorkerWorkflowExecutor,
)
from src.domain.shared.interfaces.logger import (
    AccountWorkerLogger,
    AccountWorkerLoggerFactory,
)
from src.domain.shared.interfaces.uow import Uow
from src.execution_service.settings.config import Config, config
from src.infrastructure.account_worker_logger import (
    PostgresAccountWorkerLoggerFactory,
    PostgresLogsWriter,
)
from src.infrastructure.database.repositories.account import PostgresAccountRepository
from src.infrastructure.database.repositories.account_worker import (
    PostgresAccountWorkerReader,
    PostgresAccountWorkerRepository,
)
from src.infrastructure.database.repositories.account_worker_log import (
    PostgresAccountWorkerLogRepository,
)
from src.infrastructure.database.repositories.android_device_hardware import (
    PostgresAndroidDeviceHardwareRepository,
)
from src.infrastructure.database.repositories.imap import PostgresIMAPRepository
from src.infrastructure.database.repositories.proxy import PostgresProxyRepository
from src.infrastructure.database.repositories.working_group import (
    PostgresWorkingGroupReader,
    PostgresWorkingGroupRepository,
)
from src.infrastructure.database.uow import SQLAlchemyUoW


class AccountWorkerWorkflowExecutorProvider(Provider):

    scope = Scope.APP

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_engine(
        self,
    ) -> AsyncEngine:
        return create_async_engine(
            config.db.url_sa,
            echo=False,
            pool_size=10,
            max_overflow=40,
            pool_timeout=30,
        )

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=True,
            autoflush=False,
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self,
        _sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with _sessionmaker() as session:
            yield session

    uow = provide(SQLAlchemyUoW, provides=Uow, scope=Scope.REQUEST)

    repositories = provide_all(
        WithParents[PostgresAccountRepository],
        WithParents[PostgresProxyRepository],
        WithParents[PostgresIMAPRepository],
        WithParents[PostgresWorkingGroupRepository],
        WithParents[PostgresAccountWorkerRepository],
        WithParents[PostgresAccountWorkerReader],
        WithParents[PostgresWorkingGroupReader],
        WithParents[PostgresAndroidDeviceHardwareRepository],
        scope=Scope.REQUEST,
    )

    email_service_factory = provide(EmailServiceFactory, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def proxy_provider(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> ProxyProvider:
        return ProxyProvider(
            session_factory=sessionmaker,
        )

    @provide(scope=Scope.APP)
    async def asyncio_queue(self) -> asyncio.Queue:
        return asyncio.Queue()

    @provide(scope=Scope.APP)
    async def account_worker_logs_writer(
        self,
        queue: asyncio.Queue,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> PostgresLogsWriter:
        async with sessionmaker() as session:
            uow = SQLAlchemyUoW(session)
            repository = PostgresAccountWorkerLogRepository(session)
            return PostgresLogsWriter(
                uow=uow,
                repository=repository,
                queue=queue,
            )

    @provide(scope=Scope.APP)
    async def account_worker_logger_factory(
        self, queue: asyncio.Queue
    ) -> AccountWorkerLoggerFactory:
        return PostgresAccountWorkerLoggerFactory(queue=queue)

    account_worker_id = from_context(provides=AccountWorkerID, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def account_worker_logger(
        self,
        account_worker_logger_factory: AccountWorkerLoggerFactory,
        account_worker_id: AccountWorkerID,
    ) -> AccountWorkerLogger:
        # TODO сделать чтобы логгеру можно было установить account_worker-id
        return account_worker_logger_factory.create()

    @provide(scope=Scope.REQUEST)
    async def account_worker_workflow_executor(
        self,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,
        account_repository: AccountRepository,
        working_group_repository: WorkingGroupRepository,
        android_device_hardware_repository: AndroidDeviceHardwareRepository,
        email_service_factory: EmailServiceFactory,
        proxy_provider: ProxyProvider,
        worker_logger: AccountWorkerLogger,
    ) -> AccountWorkerWorkflowExecutor:

        worker_prepare_service = AccountWorkerPrepareBeforeWorkService(
            uow=uow,
            proxy_provider=proxy_provider,
            android_device_hardware_repository=android_device_hardware_repository,
            account_worker_repository=account_worker_repository,
            worker_logger=worker_logger,
        )

        account_worker_task_executor_factory = AccountWorkerTaskExecutorFactory(
            uow=uow,
            account_repository=account_repository,
            working_group_repository=working_group_repository,
            email_service_factory=email_service_factory,
            proxy_provider=proxy_provider,
            account_worker_repository=account_worker_repository,
            worker_logger=worker_logger,
        )

        return AccountWorkerWorkflowExecutor(
            uow=uow,
            account_worker_repository=account_worker_repository,
            working_group_repository=working_group_repository,
            account_worker_task_executor_factory=account_worker_task_executor_factory,
            worker_prepare_service=worker_prepare_service,
            worker_logger=worker_logger,
        )
