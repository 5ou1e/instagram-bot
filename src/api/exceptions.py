import traceback
from collections import defaultdict
from functools import partial

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from orjson import orjson
from starlette import status

from src.api.schemas.response import ErrorResponse
from src.application.common.exceptions import (
    ApplicationError,
    IncorrectAccountStringError,
    IncorrectIMAPStringFormatError,
    IncorrectProxyStringFormatError,
)
from src.domain.shared.exceptions import DomainError


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(
        IncorrectProxyStringFormatError,
        exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        IncorrectIMAPStringFormatError,
        exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        IncorrectAccountStringError,
        exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(ApplicationError, exception_handler(500))
    app.add_exception_handler(DomainError, exception_handler(500))
    app.add_exception_handler(Exception, unknown_exception_handler)


def exception_handler(status_code: int):
    return partial(application_exception_handler, status_code=status_code)


async def application_exception_handler(
    request: Request, exc: ApplicationError | DomainError, status_code: int
) -> ORJSONResponse:
    """Обработчик ошибок приложения"""

    response = ErrorResponse(
        error=exc.title,
    )
    return ORJSONResponse(
        response.model_dump(),
        status_code=status_code,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError | Exception
) -> ORJSONResponse:
    """Обработчик ошибок валидации"""

    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(
            map(str, filtered_loc)
        )  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)
    response = ErrorResponse(
        error=f"Ошибка валидации: {orjson.dumps(reformatted_message)}"
    )

    return ORJSONResponse(
        response.model_dump(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def unknown_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    """Обработчик неизвестных ошибок"""

    traceback_str = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    )
    response = ErrorResponse(
        error=f"Внутренняя ошибка сервера: {traceback_str[-200:]}",
    )

    return ORJSONResponse(
        response.model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
