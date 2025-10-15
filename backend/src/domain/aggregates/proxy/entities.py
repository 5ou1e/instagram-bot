from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from src.domain.shared.utils import current_datetime


class ProxyProtocol(StrEnum):
    HTTP = "http"


@dataclass(kw_only=True, slots=True)
class Proxy:
    id: UUID
    protocol: ProxyProtocol = ProxyProtocol.HTTP
    host: str
    port: int
    username: str | None
    password: str | None
    usage: int | None = 0

    created_at: datetime = field(default_factory=current_datetime)
    updated_at: datetime = field(default_factory=current_datetime)

    @property
    def url(self) -> str:
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"

    @property
    def unique_key(self) -> tuple:
        return (self.protocol.value, self.host, self.port, self.username, self.password)
