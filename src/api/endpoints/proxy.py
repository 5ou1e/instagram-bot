import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body

from src.api.schemas.response import ApiResponse
from src.application.features.proxy.create_proxies import (
    CreateProxiesCommandHandler,
    CreateProxiesCommandResult,
)
from src.application.features.proxy.delete_proxies import (
    DeleteProxiesCommandHandler,
    DeleteProxiesCommandResult,
)
from src.application.features.proxy.get_proxies import (
    GetProxiesQueryHandler,
    GetProxiesQueryResult,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/proxies",
    tags=["Прокси"],
)


@router.get(
    "/",
    description="Получить список прокси",
    summary="Получить прокси",
)
@inject
async def get(
    handler: FromDishka[GetProxiesQueryHandler],
) -> ApiResponse[GetProxiesQueryResult]:
    result = await handler()
    return ApiResponse(result=result)


@router.post(
    "/",
    description="Добавить прокси",
    summary="Добавить прокси",
)
@inject
async def create(
    handler: FromDishka[CreateProxiesCommandHandler],
    data: list[str] = Body(),
) -> ApiResponse[CreateProxiesCommandResult]:
    result = await handler(data=data)
    return ApiResponse(result=result)


@router.delete(
    "/",
    description="Удалить прокси",
    summary="Удалить прокси",
)
@inject
async def delete(
    handler: FromDishka[DeleteProxiesCommandHandler],
    ids: list[UUID] | None = Body(default=None),
) -> ApiResponse[DeleteProxiesCommandResult]:
    result = await handler(ids)
    return ApiResponse(result=result)
