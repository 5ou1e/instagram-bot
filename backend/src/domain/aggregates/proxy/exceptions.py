from dataclasses import dataclass

from src.domain.shared.exceptions import DomainError


@dataclass(kw_only=True, slots=True)
class NoAvailableProxyError(DomainError):
    @property
    def title(self):
        return "Нету доступного прокси в БД"
