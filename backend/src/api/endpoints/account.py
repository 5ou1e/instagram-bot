import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body

from src.api.schemas.response import ApiResponse
from src.application.features.account.create_accounts import (
    CreateAccountsCommandHandler,
    CreateAccountsCommandResult,
)
from src.application.features.account.delete_accounts import (
    DeleteAccountsCommandHandler,
    DeleteAccountsCommandResult,
)
from src.application.features.account.get_accounts import (
    GetAccountsQueryHandler,
    GetAccountsQueryResult,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/accounts",
    tags=["Аккаунты"],
)


@router.get(
    "/",
    description="Получить аккаунты",
    summary="Получить аккаунты",
)
@inject
async def get_accounts(
    handler: FromDishka[GetAccountsQueryHandler],
) -> ApiResponse[GetAccountsQueryResult]:
    result = await handler()
    return ApiResponse(result=result)


@router.post(
    "/",
    description="Добавить аккаунты",
    summary="Добавить аккаунты",
)
@inject
async def create_accounts(
    handler: FromDishka[CreateAccountsCommandHandler],
    data: list[str] = Body(),
) -> ApiResponse[CreateAccountsCommandResult]:
    result = await handler(
        data=data,
    )
    return ApiResponse(result=result)


@router.delete(
    "/",
    description="Удалить аккаунты",
    summary="Удалить аккаунты",
)
@inject
async def delete_accounts(
    handler: FromDishka[DeleteAccountsCommandHandler],
    ids: list[UUID] | None = Body(default=None),
) -> ApiResponse[DeleteAccountsCommandResult]:
    result = await handler(ids)
    return ApiResponse(result=result)
