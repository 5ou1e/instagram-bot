from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

TResult = TypeVar("TResult")


class ApiResponse(BaseModel, Generic[TResult]):
    status: str = "success"
    result: Optional[TResult] = None


class ErrorResponse(BaseModel):
    status: str = "error"
    error: str
