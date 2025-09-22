from dataclasses import dataclass
from enum import Enum, auto

from src.domain.shared.exceptions import DomainError
from src.domain.shared.interfaces.instagram.entities.challenge import ChallengeData


class ChallengeType(Enum):
    AUTH_PLATFORM_CODE_ENTRY = auto()


@dataclass(kw_only=True, slots=True)
class InstagramError(DomainError):
    message: str | None = None

    @property
    def title(self) -> str:
        return f"Ошибка Instagram: {self.message}"


@dataclass(kw_only=True, slots=True)
class LoginRequired(InstagramError):

    @property
    def title(self) -> str:
        return f"Инстаграм сбросил авторизацию: {self.message}"


@dataclass(kw_only=True, slots=True)
class NotFoundError(InstagramError):

    @property
    def title(self) -> str:
        return f"Ресурс не найден: {self.message}"


@dataclass(kw_only=True, slots=True)
class UserIdNotFound(NotFoundError):
    user_id: str

    @property
    def title(self) -> str:
        return f"Пользователь с ID {self.user_id} не найден"


@dataclass(kw_only=True, slots=True)
class BadRequestError(InstagramError):
    @property
    def title(self) -> str:
        return f"Некорректный запрос: {self.message}"


@dataclass(kw_only=True, slots=True)
class TooManyRequestsError(InstagramError):
    @property
    def title(self) -> str:
        return f"Слишком частые запросы: {self.message}"


@dataclass(kw_only=True, slots=True)
class ChallengeRequired(InstagramError):
    challenge_data: ChallengeData

    @property
    def title(self) -> str:
        return f"Чекпоинт: {self.message}"


@dataclass(kw_only=True, slots=True)
class BadPassword(InstagramError):
    password: str

    @property
    def title(self) -> str:
        return f"Неверный пароль: {self.password}"


@dataclass(kw_only=True, slots=True)
class UnauthorizedError(InstagramError):

    @property
    def title(self) -> str:
        return f"Unauthorized: {self.message}"


@dataclass(kw_only=True, slots=True)
class NetworkError(InstagramError):
    @property
    def title(self) -> str:
        return f"Ошибка сети: {self.message}"


@dataclass(kw_only=True, slots=True)
class BadResponseError(InstagramError):
    @property
    def title(self) -> str:
        return f"Некорректный ответ от Instagram: {self.message}"


@dataclass(kw_only=True, slots=True)
class OopsAnErrorOccurred(InstagramError):
    @property
    def title(self) -> str:
        return f"Oops an error occured"


@dataclass(kw_only=True, slots=True)
class ResetPasswordError(InstagramError):
    @property
    def title(self) -> str:
        return f"Не удалось восстановить пароль: {self.message}"


@dataclass(kw_only=True, slots=True)
class EmailNotMatchedError(ResetPasswordError):
    masked_email: str
    email: str

    @property
    def title(self) -> str:
        return f"Email не соответствует: real={self.email}, masked={self.masked_email}"


@dataclass(kw_only=True, slots=True)
class ResetLinkNotSentError(ResetPasswordError):
    @property
    def title(self) -> str:
        return f"Не удалось отправить ссылку на почту: {self.message}"


@dataclass(kw_only=True, slots=True)
class ResetPasswordLinkExpiredError(ResetPasswordError):
    @property
    def title(self) -> str:
        return f"Ссылка недействительна: {self.message}"


@dataclass(kw_only=True, slots=True)
class AuthorizationError(InstagramError):
    @property
    def title(self) -> str:
        return f"Ошибка авторизации: {self.message}"


@dataclass(kw_only=True, slots=True)
class BadPasswordError(AuthorizationError):
    @property
    def title(self) -> str:
        return f"Неверный пароль"


@dataclass(kw_only=True, slots=True)
class UserNotFoundError(InstagramError):
    username: str | None = None

    @property
    def title(self) -> str:
        return f"Пользователь {self.username} не найден"


@dataclass(kw_only=True, slots=True)
class FeedbackRequiredError(InstagramError):

    @property
    def title(self) -> str:
        return f"Feedback required: {self.message}"
