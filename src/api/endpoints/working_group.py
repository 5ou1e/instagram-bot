import logging
from uuid import UUID

import aiohttp
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query

from src.api.schemas.requests.working_group_account_worker_task import (
    CreateSubtaskData,
    UpdateWorkingGroupAccountWorkerTaskData,
)
from src.api.schemas.requests.working_group_config import WorkingGroupConfigPatch
from src.api.schemas.response import ApiResponse
from src.application.common.dtos.pagination import Pagination
from src.application.common.dtos.working_group import WorkingGroupDTO, WorkingGroupsDTO
from src.application.common.types import AccountStringFormat
from src.application.features.working_group.create_working_group import (
    CreateWorkingGroupCommandHandler,
    CreateWorkingGroupCommandResult,
)
from src.application.features.working_group.delete_working_group import (
    DeleteWorkingGroupCommandHandler,
    DeleteWorkingGroupCommandResult,
)
from src.application.features.working_group.get_working_group import (
    GetWorkingGroupQueryHandler,
)
from src.application.features.working_group.get_working_groups import (
    GetWorkingGroupsQueryHandler,
)
from src.application.features.working_group.set_working_group_name import (
    SetWorkingGroupNameCommand,
    SetWorkingGroupNameCommandHandler,
)
from src.application.features.working_group.update_working_group_config import (
    UpdateWorkingGroupConfigCommand,
    UpdateWorkingGroupConfigCommandHandler,
    UpdateWorkingGroupConfigCommandResult,
)
from src.application.features.working_group.worker.create_workers import (
    CreateWorkingGroupWorkersCommandCommandResult,
    CreateWorkingGroupWorkersCommandHandler,
)
from src.application.features.working_group.worker.delete_workers import (
    DeleteWorkingGroupWorkersCommandHandler,
    DeleteWorkingGroupWorkersCommandResult,
)
from src.application.features.working_group.worker.dto import WorkingGroupWorkersDTO
from src.application.features.working_group.worker.get_workers import (
    GetWorkingGroupWorkersQuery,
    GetWorkingGroupWorkersQueryHandler,
)
from src.application.features.working_group.worker_task.create_worker_task import (
    CreateWorkerTaskCommand,
    CreateWorkerTaskCommandHandler,
)
from src.application.features.working_group.worker_task.delete_worker_task import (
    DeleteWorkingGroupWorkerTaskCommand,
    DeleteWorkingGroupWorkerTaskCommandHandler,
)
from src.application.features.working_group.worker_task.update_worker_task import (
    UpdateWorkingGroupAccountWorkerTaskCommand,
    UpdateWorkingGroupAccountWorkerTaskCommandHandler,
    UpdateWorkingGroupAccountWorkerTaskCommandResult,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/working_groups",
    tags=["Рабочие группы аккаунтов"],
)


@router.get(
    "/{wg_id}/",
    description="Получить рабочую группу по ID",
    summary="Получить рабочую группу по ID",
)
@inject
async def get_working_group_by_id(
    wg_id: UUID,
    handler: FromDishka[GetWorkingGroupQueryHandler],
) -> ApiResponse[WorkingGroupDTO]:
    result = await handler(working_group_id=wg_id)
    return ApiResponse(result=result)


@router.get(
    "/",
    description="Получить список рабочих групп",
    summary="Получить список рабочих групп",
)
@inject
async def get_working_groups(
    handler: FromDishka[GetWorkingGroupsQueryHandler],
) -> ApiResponse[WorkingGroupsDTO]:

    result = await handler()
    return ApiResponse(result=result)


@router.post(
    "/",
    description="Создать рабочую группу",
    summary="Создать рабочую группу",
)
@inject
async def create_working_group(
    handler: FromDishka[CreateWorkingGroupCommandHandler],
    name: str = Body(embed=True),
) -> ApiResponse[CreateWorkingGroupCommandResult]:
    result = await handler(
        name=name,
    )
    return ApiResponse(result=result)


@router.delete(
    "/{wg_id}/",
    description="Удалить рабочую группу по ID",
    summary="Удалить рабочую группу по ID",
)
@inject
async def delete_working_group(
    handler: FromDishka[DeleteWorkingGroupCommandHandler],
    wg_id: UUID,
) -> ApiResponse[DeleteWorkingGroupCommandResult]:
    result = await handler(working_group_id=wg_id)
    return ApiResponse(result=result)


@router.get(
    "/{wg_id}/workers/",
    description="Получить аккаунты рабочей группы",
    summary="Получить аккаунты рабочей группы",
)
@inject
async def get_working_group_account_workers(
    wg_id: UUID,
    handler: FromDishka[GetWorkingGroupWorkersQueryHandler],
    page: int = Query(1, ge=1, description="Номер страницы, минимум 1"),
    page_size: int = Query(
        10, ge=1, le=10_000, description="Размер страницы (1–10000)"
    ),
) -> ApiResponse[WorkingGroupWorkersDTO]:

    result = await handler(
        GetWorkingGroupWorkersQuery(
            working_group_id=wg_id,
            pagination=Pagination(
                page=page,
                page_size=page_size,
            ),
        )
    )
    return ApiResponse(result=result)


@router.post(
    "/{wg_id}/workers/",
    description="Добавить аккаунты в рабочую группу",
    summary="Добавить аккаунты в рабочую группу",
)
@inject
async def create_working_group_account_workers(
    handler: FromDishka[CreateWorkingGroupWorkersCommandHandler],
    wg_id: UUID,
    worker_strings: list[str] = Body(embed=True),
    format: AccountStringFormat = Body(embed=True),
) -> ApiResponse[CreateWorkingGroupWorkersCommandCommandResult]:

    result = await handler(
        working_group_id=wg_id,
        format_=format,
        account_worker_strings=worker_strings,
    )
    return ApiResponse(result=result)


@router.delete(
    "/{wg_id}/workers/",
    description="Удалить аккаунты из рабочей группы",
    summary="Удалить аккаунты из рабочей группы",
)
@inject
async def delete_workers(
    handler: FromDishka[DeleteWorkingGroupWorkersCommandHandler],
    wg_id: UUID,
    worker_ids: list[str] | None = Body(default=None, embed=True),
) -> ApiResponse[DeleteWorkingGroupWorkersCommandResult]:
    result = await handler(working_group_id=wg_id, worker_ids=worker_ids)
    return ApiResponse(result=result)


@router.post(
    "/{wg_id}/start_workers/",
    description="Запустить аккаунты",
    summary="Запустить аккаунты",
)
@inject
async def start_workers(
    wg_id: UUID,
    worker_ids: list[UUID] = Body(embed=True),
) -> ApiResponse:
    SERVICE_URL = "http://127.0.0.1:8001/executions/start_workers"

    data = {"worker_ids": [str(w_id) for w_id in worker_ids]}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=SERVICE_URL,
            json=data,
        ) as response:
            text = await response.text()
            print(text)

    return ApiResponse()


@router.patch(
    "/{wg_id}/config/",
    description="Обновить конфиг рабочей группы",
    summary="Обновить конфиг рабочей группы",
)
@inject
async def patch_working_group_config(
    handler: FromDishka[UpdateWorkingGroupConfigCommandHandler],
    wg_id: UUID,
    data: WorkingGroupConfigPatch = Body(),
) -> ApiResponse[UpdateWorkingGroupConfigCommandResult]:
    result = await handler(
        UpdateWorkingGroupConfigCommand(
            working_group_id=wg_id,
            data=data.model_dump(exclude_unset=True),
        )
    )
    return ApiResponse(result=result)


@router.put(
    "/{wg_id}/name/",
    description="Обновить имя рабочей группы",
    summary="Обновить имя рабочей группы",
)
@inject
async def put_working_group_name(
    handler: FromDishka[SetWorkingGroupNameCommandHandler],
    wg_id: UUID,
    name: str = Body(),
) -> ApiResponse:
    result = await handler(
        SetWorkingGroupNameCommand(
            working_group_id=wg_id,
            name=name,
        )
    )
    return ApiResponse(result=result)


@router.post(
    "/{wg_id}/worker_tasks/",
    description="Создать задачу для аккаунтов",
    summary="Создать задачу для аккаунтов",
)
@inject
async def create_working_group_account_worker_task(
    handler: FromDishka[CreateWorkerTaskCommandHandler],
    wg_id: UUID,
    data: CreateSubtaskData = Body(),
) -> ApiResponse:

    result = await handler(
        command=CreateWorkerTaskCommand(
            working_group_id=wg_id,
            type=data.type,
            name=data.name,
            enabled=data.enabled,
            index=data.index,
            config=data.config.model_dump() if data.config else {},
        ),
    )
    return ApiResponse(result=result)


@router.delete(
    "/{wg_id}/worker_tasks/{task_id}",
    description="Удалить задачу для аккаунтов",
    summary="Удалить задачу для аккаунтов",
)
@inject
async def delete_working_group_account_worker_task(
    handler: FromDishka[DeleteWorkingGroupWorkerTaskCommandHandler],
    wg_id: UUID,
    subtask_id: UUID,
) -> ApiResponse:
    result = await handler(
        command=DeleteWorkingGroupWorkerTaskCommand(
            working_group_id=wg_id,
            subtask_id=subtask_id,
        ),
    )
    return ApiResponse(result=result)


@router.patch(
    "/{wg_id}/worker_tasks/{task_id}/",
    description="Обновить задачу для аккаунтов",
    summary="Обновить задачу для аккаунтов",
)
@inject
async def patch_account_worker_task(
    handler: FromDishka[UpdateWorkingGroupAccountWorkerTaskCommandHandler],
    wg_id: UUID,
    task_id: UUID,
    data: UpdateWorkingGroupAccountWorkerTaskData = Body(),
) -> ApiResponse[UpdateWorkingGroupAccountWorkerTaskCommandResult]:
    result = await handler(
        UpdateWorkingGroupAccountWorkerTaskCommand(
            working_group_id=wg_id,
            task_id=task_id,
            **data.model_dump(exclude_unset=True),
        ),
    )
    return ApiResponse(result=result)
