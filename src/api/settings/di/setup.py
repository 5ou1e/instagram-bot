from dishka import AsyncContainer, make_async_container

from src.api.settings.config import Config, config
from src.api.settings.di.provider import AppProvider


def create_async_app_container() -> AsyncContainer:
    """Контейнер FastAPI приложения"""

    return make_async_container(
        AppProvider(),
        context={Config: config},
    )
