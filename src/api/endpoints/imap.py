import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body

from src.api.schemas.response import ApiResponse
from src.application.features.imap.create_imaps import (
    CreateIMAPsCommandHandler,
    CreateIMAPsCommandResult,
)
from src.application.features.imap.delete_imaps import (
    DeleteIMAPsCommandHandler,
    DeleteIMAPsCommandResult,
)
from src.application.features.imap.get_imaps import (
    GetIMAPsQueryHandler,
    GetIMAPsQueryResult,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/imaps",
    tags=["IMAPs"],
)


@router.get(
    "/",
    description="Получить список IMAP-серверов",
    summary="Получить IMAPs",
)
@inject
async def get(
    handler: FromDishka[GetIMAPsQueryHandler],
) -> ApiResponse[GetIMAPsQueryResult]:
    result = await handler()
    return ApiResponse(result=result)


@router.post(
    "/",
    description="Добавить IMAP-серверы",
    summary="Добавить IMAPs",
)
@inject
async def create(
    handler: FromDishka[CreateIMAPsCommandHandler],
    data: list[str] = Body(),
) -> ApiResponse[CreateIMAPsCommandResult]:
    result = await handler(data=data)
    return ApiResponse(result=result)


@router.delete(
    "/",
    description="Удалить IMAP-серверы",
    summary="Удалить IMAPs",
)
@inject
async def delete(
    handler: FromDishka[DeleteIMAPsCommandHandler],
    ids: list[UUID] | None = Body(default=None),
) -> ApiResponse[DeleteIMAPsCommandResult]:
    result = await handler(ids)
    return ApiResponse(result=result)
