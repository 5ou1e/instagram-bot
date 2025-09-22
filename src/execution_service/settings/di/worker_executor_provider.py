import asyncio
from typing import AsyncIterable

from dishka import Provider, Scope, WithParents, from_context, provide, provide_all
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.api.settings.config import Config, config
from src.domain.account.repositories.account import AccountRepository
from src.domain.android_device.repository import AndroidDeviceHardwareRepository
from src.domain.shared.interfaces.logger import AccountWorkerLoggerFactory
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.services.email_service import EmailServiceFactory
from src.domain.working_group.repositories.account_worker import AccountWorkerRepository
from src.domain.working_group.repositories.account_worker_task import (
    AccountWorkerTaskRepository,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.domain.working_group.services.providers.proxy_provider import ProxyProvider
from src.domain.working_group.services.task_executors.executor_factory import (
    AccountWorkerTaskExecutorFactory,
)
from src.domain.working_group.services.worker_prepare_service import (
    AccountWorkerPrepareBeforeWorkService,
)
from src.domain.working_group.services.worker_workflow_executor import (
    AccountWorkerWorkflowExecutor,
)
from src.infrastructure.account_worker_logger import (
    PostgresAccountWorkerLoggerFactory,
    PostgresLogsWriter,
)
from src.infrastructure.database.repositories.account import PostgresAccountRepository
from src.infrastructure.database.repositories.android_device import (
    PostgresAndroidDeviceHardwareRepository,
)
from src.infrastructure.database.repositories.imap import PostgresIMAPRepository
from src.infrastructure.database.repositories.log import PostgresLogRepository
from src.infrastructure.database.repositories.proxy import PostgresProxyRepository
from src.infrastructure.database.repositories.working_group import (
    PostgresWorkingGroupReader,
    PostgresWorkingGroupRepository,
)
from src.infrastructure.database.repositories.working_group_worker import (
    PostgresAccountWorkerReader,
    PostgresAccountWorkerRepository,
)
from src.infrastructure.database.repositories.working_group_worker_task import (
    PostgresAccountWorkerTaskRepository,
)
from src.infrastructure.database.uow import SQLAlchemyUoW
from src.infrastructure.files.file import File
from src.infrastructure.files.file_writer import (
    AccountResetPassFailedResultFileWriter,
    AccountResetPassSuccessResultFileWriter,
)


class TaskWorkerProvider(Provider):

    scope = Scope.APP

    config = from_context(provides=Config, scope=Scope.APP)

    # Db
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
        WithParents[PostgresAccountWorkerTaskRepository],
        WithParents[PostgresAndroidDeviceHardwareRepository],
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.APP)
    async def success_writer(self) -> AccountResetPassSuccessResultFileWriter:
        return AccountResetPassSuccessResultFileWriter(
            File(config.files.accounts_reset_pass_success_filepath)
        )

    @provide(scope=Scope.APP)
    async def failed_writer(self) -> AccountResetPassFailedResultFileWriter:
        return AccountResetPassFailedResultFileWriter(
            File(config.files.accounts_reset_pass_failed_filepath)
        )

    @provide(scope=Scope.APP)
    async def asyncio_queue(self) -> asyncio.Queue:
        return asyncio.Queue()

    @provide(scope=Scope.APP)
    async def account_logs_writer(
        self,
        queue: asyncio.Queue,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> PostgresLogsWriter:
        async with sessionmaker() as session:
            uow = SQLAlchemyUoW(session)
            repository = PostgresLogRepository(session)
            return PostgresLogsWriter(
                uow=uow,
                repository=repository,
                queue=queue,
            )

    @provide(scope=Scope.APP)
    async def account_logger_factory(
        self, queue: asyncio.Queue
    ) -> AccountWorkerLoggerFactory:
        return PostgresAccountWorkerLoggerFactory(queue=queue)

    email_service_factory = provide(EmailServiceFactory, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def proxy_provider(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> ProxyProvider:
        return ProxyProvider(
            session_factory=sessionmaker,
        )

    @provide(scope=Scope.REQUEST)
    async def worker_workflow_executor(
        self,
        logger_factory: AccountWorkerLoggerFactory,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,
        account_repository: AccountRepository,
        working_group_repository: WorkingGroupRepository,
        account_worker_task_repository: AccountWorkerTaskRepository,
        android_device_hardware_repository: AndroidDeviceHardwareRepository,
        email_service_factory: EmailServiceFactory,
        proxy_provider: ProxyProvider,
        account_reset_password_success_writer: AccountResetPassSuccessResultFileWriter,
        account_reset_password_failed_writer: AccountResetPassFailedResultFileWriter,
    ) -> AccountWorkerWorkflowExecutor:

        worker_prepare_service = AccountWorkerPrepareBeforeWorkService(
            uow=uow,
            proxy_provider=proxy_provider,
            android_device_hardware_repository=android_device_hardware_repository,
            account_worker_repository=account_worker_repository,
        )

        account_worker_task_executor_factory = AccountWorkerTaskExecutorFactory(
            uow=uow,
            account_repository=account_repository,
            account_worker_task_repository=account_worker_task_repository,
            working_group_repository=working_group_repository,
            email_service_factory=email_service_factory,
            proxy_provider=proxy_provider,
            account_reset_password_success_writer=account_reset_password_success_writer,
            account_reset_password_failed_writer=account_reset_password_failed_writer,
            account_worker_repository=account_worker_repository,
        )

        # MockWorkerWorkflowExecutor
        return AccountWorkerWorkflowExecutor(  # noqa
            uow=uow,
            account_worker_repository=account_worker_repository,
            account_repository=account_repository,
            working_group_repository=working_group_repository,
            logger_factory=logger_factory,
            account_worker_task_executor_factory=account_worker_task_executor_factory,
            worker_prepare_service=worker_prepare_service,
        )
