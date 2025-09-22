import logging
from contextlib import asynccontextmanager
from uuid import UUID

import uvicorn
from dishka import FromDishka
from dishka.integrations.fastapi import inject, setup_dishka
from fastapi import APIRouter, Body, FastAPI
from fastapi.responses import RedirectResponse

from src.execution_service.handlers.start_worker import (
    StartWorkersCommand,
    StartWorkersCommandHandler,
)
from src.execution_service.handlers.stop_worker import (
    StopWorkersCommand,
    StopWorkersCommandHandler,
)
from src.execution_service.settings.di.setup import create_execution_service_container
from src.execution_service.settings.logging import setup_logging

router = APIRouter(prefix="/executions")


@router.post("/start_workers", status_code=202)
@inject
async def start_workers(
    handler: FromDishka[StartWorkersCommandHandler],
    worker_ids: list[UUID] = Body(embed=True),
):
    await handler(StartWorkersCommand(worker_ids=worker_ids))


@router.post("/stop_workers/", status_code=202)
@inject
async def stop_workers(
    handler: FromDishka[StopWorkersCommandHandler],
    worker_ids: list[UUID] = Body(embed=True),
):
    await handler(StopWorkersCommand(worker_ids=worker_ids))


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()  # noqa


app = FastAPI(
    title="Execution Service API",
    lifespan=lifespan,
)

app.include_router(router)
setup_dishka(create_execution_service_container(), app)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    setup_logging(level=logging.DEBUG)
    uvicorn.run(
        "src.infrastructure.execution_service.api.main:app",  # путь до app
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
