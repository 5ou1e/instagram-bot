from dataclasses import dataclass

from src.domain.shared.exceptions import DomainError


@dataclass(kw_only=True, slots=True)
class ApplicationError(DomainError):

    @property
    def title(self) -> str:
        return "Ошибка приложения"

    def __str__(self) -> str:
        return self.title


@dataclass(kw_only=True, slots=True)
class IncorrectProxyStringFormatError(ApplicationError):
    string: str

    @property
    def title(self) -> str:
        return f"Некорректный формат Proxy : {self.string}"


@dataclass(kw_only=True, slots=True)
class IncorrectIMAPStringFormatError(ApplicationError):
    string: str

    @property
    def title(self) -> str:
        return f"Некорректный формат IMAP : {self.string}"


@dataclass(kw_only=True, slots=True)
class IncorrectAccountStringError(ApplicationError):
    string: str

    @property
    def title(self) -> str:
        return f"Некорректная строка с аккаунтом: {self.string}"


@dataclass(kw_only=True, slots=True)
class InvalidWorkingGroupConfigDataError(ApplicationError):
    config_data: dict

    @property
    def title(self) -> str:
        return f"Некорректный формат конфига: {self.config_data}"


@dataclass(kw_only=True, slots=True)
class IncorrectAndroidUserAgentString(ApplicationError):
    string: str

    @property
    def title(self) -> str:
        return f"Некорректный формат android user-agent : {self.string}"
