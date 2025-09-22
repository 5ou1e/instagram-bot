import logging
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body

from src.api.schemas.response import ApiResponse
from src.application.features.android_device.create_android_device_hardwares_from_user_agents import (
    CreateAndroidDeviceHardwaresFromUserAgentsCommandHandler,
    CreateAndroidDeviceHardwaresFromUserAgentsCommandResult,
)
from src.application.features.android_device.delete_android_device_hardwares import (
    DeleteAndroidDeviceHardwaresCommandHandler,
)
from src.application.features.android_device.get_android_device_hardwares import (
    GetAndroidDeviceHardwaresQueryHandler,
    GetAndroidDeviceHardwaresQueryResult,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/android_devices",
    tags=["Android-устройства"],
)


@router.get(
    "/",
    description="Получить виды android-устройств",
    summary="Получить виды android-устройств",
)
@inject
async def get(
    handler: FromDishka[GetAndroidDeviceHardwaresQueryHandler],
) -> ApiResponse[GetAndroidDeviceHardwaresQueryResult]:
    result = await handler()
    return ApiResponse(result=result)


@router.post(
    "/",
    description="Cоздать виды android-устройств из юзер-агентов",
    summary="Cоздать виды android-устройств из юзер-агентов",
)
@inject
async def create(
    handler: FromDishka[CreateAndroidDeviceHardwaresFromUserAgentsCommandHandler],
    data: list[str] = Body(),
) -> ApiResponse[CreateAndroidDeviceHardwaresFromUserAgentsCommandResult]:
    result = await handler(data=data)
    return ApiResponse(result=result)


@router.delete(
    "/",
    description="Удалить виды android-устройств",
    summary="Удалить виды android-устройств",
)
@inject
async def delete(
    handler: FromDishka[DeleteAndroidDeviceHardwaresCommandHandler],
    ids: list[UUID] | None = Body(default=None),
) -> ApiResponse:
    result = await handler(ids)
    return ApiResponse(result=result)
