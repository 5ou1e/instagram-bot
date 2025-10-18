import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query

from src.api.schemas.response import ApiResponse
from src.application.common.dtos.pagination import Pagination
from src.application.features.proxy.create_proxies import (
    CreateProxiesCommandHandler,
    CreateProxiesCommandResult,
)
from src.application.features.proxy.delete_proxies import (
    DeleteProxiesCommandHandler,
    DeleteProxiesCommandResult,
)
from src.application.features.proxy.get_proxies import (
    GetProxiesQuery,
    GetProxiesQueryHandler,
    ProxiesDTO,
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
    page: int = Query(1, ge=1, description="Номер страницы, минимум 1"),
    page_size: int = Query(
        10, ge=1, le=10_000, description="Размер страницы (1–10000)"
    ),
) -> ApiResponse[ProxiesDTO]:
    result = await handler(
        GetProxiesQuery(
            pagination=Pagination(
                page=page,
                page_size=page_size,
            ),
        )
    )
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
    ids: list[UUID] | None = Body(default=None, embed=True),
) -> ApiResponse[DeleteProxiesCommandResult]:
    result = await handler(ids)
    return ApiResponse(result=result)
