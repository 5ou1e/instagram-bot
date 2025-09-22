import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query

from src.api.schemas.response import ApiResponse
from src.application.features.log.delete_logs import (
    DeleteLogsCommandHandler,
    DeleteLogsCommandResult,
)
from src.application.features.log.get_logs import (
    GetLogsQueryHandler,
    GetLogsQueryResult,
)
from src.domain.account.entities.account_log import AccountWorkerLogType

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/logs",
    tags=["Логи"],
)


@router.get(
    "/",
    description="Получить логи аккаунтов",
    summary="Получить логи аккаунтов",
)
@inject
async def get_logs(
    handler: FromDishka[GetLogsQueryHandler],
    account_ids: list[UUID] = Query(default=None),
    types: list[AccountWorkerLogType] = Query(default=None),
) -> ApiResponse[GetLogsQueryResult]:
    result = await handler(
        account_ids=account_ids,
        types=types,
    )
    return ApiResponse(result=result)


@router.delete(
    "/",
    description="Удалить логи аккаунтов",
    summary="Удалить логи аккаунтов",
)
@inject
async def delete_logs(
    handler: FromDishka[DeleteLogsCommandHandler],
    account_ids: list[UUID] | None = Body(default=None, embed=True),
) -> ApiResponse[DeleteLogsCommandResult]:

    result = await handler(
        account_ids=account_ids,
    )
    return ApiResponse(result=result)
