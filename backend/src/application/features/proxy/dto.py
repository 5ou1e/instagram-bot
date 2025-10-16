from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.application.common.dtos.pagination import PaginationResult


@dataclass(kw_only=True, slots=True)
class ProxyDTO:
    id: UUID
    protocol: str
    host: str
    port: int
    username: str
    password: str

    created_at: datetime


@dataclass
class ProxiesDTO:
    proxies: list[ProxyDTO]
    pagination: PaginationResult
