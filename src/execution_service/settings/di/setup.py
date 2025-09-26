from dishka import AsyncContainer, make_async_container

from src.execution_service.settings.config import Config, config
from src.api.settings.di.provider import AppProvider
from src.execution_service.settings.di.execution_service_provider import (
    ExecutionServiceProvider,
)
from src.execution_service.settings.di.worker_executor_provider import (
    TaskWorkerProvider,
)


def create_async_app_container() -> AsyncContainer:
    """Контейнер FastAPI приложения"""

    return make_async_container(
        AppProvider(),
        context={Config: config},
    )


def create_execution_service_container() -> AsyncContainer:

    return make_async_container(
        ExecutionServiceProvider(),
        context={Config: config},
    )


def create_workers_manager_container() -> AsyncContainer:
    """Контейнер для TaskWorker-а
    Под каждый процесс, обрабатывающий аккаунты в задаче , создается свой контейнер
    """

    return make_async_container(
        TaskWorkerProvider(),
        context={Config: config},
    )
