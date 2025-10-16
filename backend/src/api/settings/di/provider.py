from typing import AsyncIterable

from dishka import Provider, Scope, WithParents, from_context, provide, provide_all
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.api.settings.config import Config, config
from src.application.features.account.create_accounts import (
    CreateAccountsCommandHandler,
)
from src.application.features.account.delete_accounts import (
    DeleteAccountsCommandHandler,
)
from src.application.features.account.get_accounts import GetAccountsQueryHandler
from src.application.features.account.set_accounts_comment import SetAccountsCommentCommandHandler
from src.application.features.android_device.create_android_device_hardwares_from_user_agents import (
    CreateAndroidDeviceHardwaresFromUserAgentsCommandHandler,
)
from src.application.features.android_device.delete_android_device_hardwares import (
    DeleteAndroidDeviceHardwaresCommandHandler,
)
from src.application.features.android_device.get_android_device_hardwares import (
    GetAndroidDeviceHardwaresQueryHandler,
)
from src.application.features.imap.create_imaps import CreateIMAPsCommandHandler
from src.application.features.imap.delete_imaps import DeleteIMAPsCommandHandler
from src.application.features.imap.get_imaps import GetIMAPsQueryHandler
from src.application.features.log.delete_logs import DeleteLogsCommandHandler
from src.application.features.log.get_logs import GetLogsQueryHandler
from src.application.features.proxy.create_proxies import CreateProxiesCommandHandler
from src.application.features.proxy.delete_proxies import DeleteProxiesCommandHandler
from src.application.features.proxy.get_proxies import GetProxiesQueryHandler
from src.application.features.working_group.account_worker.create_workers import (
    CreateWorkingGroupWorkersCommandHandler,
)
from src.application.features.working_group.account_worker.delete_workers import (
    DeleteWorkingGroupWorkersCommandHandler,
)
from src.application.features.working_group.account_worker.get_workers import (
    GetWorkingGroupWorkersQueryHandler,
)
from src.application.features.working_group.create_working_group import (
    CreateWorkingGroupCommandHandler,
)
from src.application.features.working_group.delete_working_group import (
    DeleteWorkingGroupCommandHandler,
)
from src.application.features.working_group.get_working_group import (
    GetWorkingGroupQueryHandler,
)
from src.application.features.working_group.get_working_groups import (
    GetWorkingGroupsQueryHandler,
)
from src.application.features.working_group.set_working_group_name import (
    SetWorkingGroupNameCommandHandler,
)
from src.application.features.working_group.update_working_group_config import (
    UpdateWorkingGroupConfigCommandHandler,
)
from src.application.features.working_group.worker_task.create_worker_task import (
    CreateWorkerTaskCommandHandler,
)
from src.application.features.working_group.worker_task.delete_worker_task import (
    DeleteWorkingGroupWorkerTaskCommandHandler,
)
from src.application.features.working_group.worker_task.update_worker_task import (
    UpdateWorkingGroupAccountWorkerTaskCommandHandler,
)
from src.domain.shared.interfaces.uow import Uow
from src.infrastructure.database.repositories.account import PostgresAccountRepository
from src.infrastructure.database.repositories.account_worker import (
    PostgresAccountWorkerReader,
    PostgresAccountWorkerRepository,
)
from src.infrastructure.database.repositories.account_worker_log import (
    PostgresAccountWorkerLogRepository,
)
from src.infrastructure.database.repositories.android_device import (
    PostgresAndroidDeviceRepository,
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


class AppProvider(Provider):
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
            pool_size=config.db.min_size,
            max_overflow=config.db.max_size,
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
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    uow = provide(SQLAlchemyUoW, provides=Uow, scope=Scope.REQUEST)

    repositories = provide_all(
        WithParents[PostgresAccountRepository],
        WithParents[PostgresProxyRepository],
        WithParents[PostgresAndroidDeviceRepository],
        WithParents[PostgresAndroidDeviceHardwareRepository],
        WithParents[PostgresIMAPRepository],
        WithParents[PostgresAccountWorkerLogRepository],
        WithParents[PostgresWorkingGroupRepository],
        WithParents[PostgresAccountWorkerRepository],
        WithParents[PostgresAccountWorkerReader],
        WithParents[PostgresWorkingGroupReader],
        scope=Scope.REQUEST,
    )

    handlers = provide_all(
        # Accounts
        GetAccountsQueryHandler,
        CreateAccountsCommandHandler,
        DeleteAccountsCommandHandler,
        SetAccountsCommentCommandHandler,
        # Proxies
        GetProxiesQueryHandler,
        CreateProxiesCommandHandler,
        DeleteProxiesCommandHandler,
        # AdroidDevices
        GetAndroidDeviceHardwaresQueryHandler,
        CreateAndroidDeviceHardwaresFromUserAgentsCommandHandler,
        DeleteAndroidDeviceHardwaresCommandHandler,
        # IMAP
        GetIMAPsQueryHandler,
        CreateIMAPsCommandHandler,
        DeleteIMAPsCommandHandler,
        # Logs
        GetLogsQueryHandler,
        DeleteLogsCommandHandler,
        # Working Groups
        GetWorkingGroupQueryHandler,
        GetWorkingGroupsQueryHandler,
        CreateWorkingGroupCommandHandler,
        DeleteWorkingGroupCommandHandler,
        # Working Group's workers
        GetWorkingGroupWorkersQueryHandler,
        CreateWorkingGroupWorkersCommandHandler,
        DeleteWorkingGroupWorkersCommandHandler,
        SetWorkingGroupNameCommandHandler,
        UpdateWorkingGroupConfigCommandHandler,
        # WorkingGroupAccountWorkerTasks
        CreateWorkerTaskCommandHandler,
        UpdateWorkingGroupAccountWorkerTaskCommandHandler,
        DeleteWorkingGroupWorkerTaskCommandHandler,
        scope=Scope.REQUEST,
    )
