from fastapi import APIRouter

from src.api.endpoints import (
    account_router,
    android_devices_router,
    imap_router,
    log_router,
    proxy_router,
    tasks_router,
)
from src.api.endpoints.default import docs_router, root_router
from src.api.settings.config import config


def setup_v1_router():
    """Конфигурация v1 роутера"""
    v1_router = APIRouter(prefix=config.api.v1.prefix)
    v1_router_list = [
        tasks_router,
        account_router,
        proxy_router,
        android_devices_router,
        log_router,
        imap_router,
    ]
    for router in v1_router_list:
        v1_router.include_router(router)

    return v1_router


def setup_api_router(app):
    """Подключение API-роутеров"""

    v1_router = setup_v1_router()

    api_router = APIRouter(prefix=config.api.prefix)

    api_router.include_router(docs_router)
    api_router.include_router(v1_router)

    app.include_router(api_router)


def setup_routers(app) -> None:
    """Подключение всех роутеров."""

    app.include_router(root_router)
    setup_api_router(app)
