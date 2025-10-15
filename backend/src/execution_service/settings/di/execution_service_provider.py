from typing import AsyncIterable

from dishka import Provider, Scope, from_context, provide, provide_all
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.domain.shared.interfaces.uow import Uow
from src.execution_service.handlers.start_worker import StartWorkersCommandHandler
from src.execution_service.handlers.stop_worker import StopWorkersCommandHandler
from src.execution_service.services.worker_workflow_executors_manager import (
    WorkerWorkflowExecutorsManager,
)
from src.execution_service.settings.config import Config, config
from src.infrastructure.database.uow import SQLAlchemyUoW


class ExecutionServiceProvider(Provider):
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

    workers_manager = provide(WorkerWorkflowExecutorsManager, scope=Scope.APP)

    handlers = provide_all(
        StartWorkersCommandHandler,
        StopWorkersCommandHandler,
    )
