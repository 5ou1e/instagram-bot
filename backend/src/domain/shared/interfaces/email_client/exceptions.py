from dataclasses import dataclass

from src.domain.shared.exceptions import DomainError


@dataclass(kw_only=True, slots=True)
class EmailClientError(DomainError):
    @property
    def title(self):
        return "Ошибка Email-клиента"


@dataclass(kw_only=True, slots=True)
class EmailAuthenticationFailed(EmailClientError):
    message: str | None = None

    @property
    def title(self):
        return f"Не удалось авторизоваться в почте: {self.message}"


@dataclass(kw_only=True, slots=True)
class BadEmailError(EmailClientError):
    email: str

    @property
    def title(self):
        return f"Некорректная строка email: {self.email}"


@dataclass(kw_only=True, slots=True)
class PasswordChangeMessageNotFound(DomainError):
    @property
    def title(self):
        return "Сообщение для смены пароля на почте не найдено"


@dataclass(kw_only=True, slots=True)
class AuthPlatformChallengeCodeNotFound(DomainError):
    @property
    def title(self):
        return "Код на почте не найден"


@dataclass(kw_only=True, slots=True)
class IncorrectEmailStringError(DomainError):
    email: str

    @property
    def title(self):
        return f"Некорректная строка email: {self.email}"
