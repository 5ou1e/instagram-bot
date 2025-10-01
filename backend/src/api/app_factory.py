from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse

from src.api.exceptions import setup_exception_handlers
from src.api.middlewares import setup_middlewares
from src.api.routers import setup_routers
from src.api.settings.config import config
from src.api.settings.di.setup import create_async_app_container
from src.api.settings.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()  # noqa


class AppFactory:
    """Создает приложение FastAPI"""

    @staticmethod
    def create_app() -> FastAPI:

        app: FastAPI = FastAPI(
            lifespan=lifespan,
            default_response_class=ORJSONResponse,
            title="Insta API",
            openapi_url=f"{config.api.prefix}/openapi.json",
            docs_url=f"{config.api.prefix}/docs",
            redoc_url=f"{config.api.prefix}/redoc",
            swagger_ui_parameters={
                "persistAuthorization": True,
                "syntaxHighlight": False,
            },  # Сохраняет авторизацию при перезагрузке страницы доки
        )

        setup_routers(app)
        setup_middlewares(app)
        setup_exception_handlers(app)
        setup_openapi(app)
        setup_logging()

        setup_dishka(create_async_app_container(), app)

        return app


def setup_openapi(app: FastAPI):
    def custom_openapi():
        if not app.openapi_schema:
            app.openapi_schema = get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                terms_of_service=app.terms_of_service,
                contact=app.contact,
                license_info=app.license_info,
                routes=app.routes,
                tags=app.openapi_tags,
                servers=app.servers,
            )
            for _, method_item in app.openapi_schema.get("paths").items():
                for _, param in method_item.items():
                    responses = param.get("responses")
                    # remove 422 response, also can remove other status code
                    if "422" in responses:
                        del responses["422"]

            # # Добавляем ErrorResponse как описание для 400 и 500 ко всем методам
            # for path_item in app.openapi_schema["paths"].values():
            #     for operation in path_item.values():
            #         responses = operation.setdefault("responses", {})
            #         for status_code in ["404", "422", "500"]:
            #             responses.setdefault(status_code, {
            #                 "description": "Error",
            #                 "content": {
            #                     "application/json": {
            #                         "schema": ErrorResponse.schema()
            #                     }
            #                 }
            #             })

        return app.openapi_schema

    app.openapi = custom_openapi
