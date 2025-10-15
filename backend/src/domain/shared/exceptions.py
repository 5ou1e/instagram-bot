from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class DomainError(Exception):

    @property
    def title(self) -> str:
        return f"Доменная ошибка"

    def __str__(self) -> str:
        return self.title


@dataclass(kw_only=True, slots=True)
class InvalidStateTransitionError(DomainError):
    action: str
    state: str
    state: str

    @property
    def title(self) -> str:
        return f"Нельзя выполнить действие '{self.action}' из состояния '{self.state}'"
