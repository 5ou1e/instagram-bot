import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AccountWorkerTaskType(Enum):
    AUTHORIZE_ACCOUNT = "AUTHORIZE_ACCOUNT"
    RESET_PASSWORD_BY_EMAIL = "RESET_PASSWORD_BY_EMAIL"
    ACTIONS_WITH_USERS = "ACTIONS_WITH_USERS"
    DO_TASKS_FROM_BOOST_SERVICES = "DO_TASKS_FROM_BOOST_SERVICES"

    def __init__(self, value):
        self._default_name = {
            "RESET_PASSWORD_BY_EMAIL": "Восстановить пароль через email",
            "AUTHORIZE_ACCOUNT": "Авторизовать аккаунт",
            "ACTIONS_WITH_USERS": "Действия с пользователями",
            "DO_TASKS_FROM_BOOST_SERVICES": f"Выполнять задания с сервисов",
        }[value]

    @property
    def default_name(self):
        return self._default_name


@dataclass(kw_only=True)
class AccountWorkerTask:
    """Базовый класс задачи воркера"""

    id: uuid.UUID
    type: AccountWorkerTaskType
    name: Optional[str] = None
    enabled: bool = False
    index: int = 0
    config: dict = field(default_factory=dict)
    working_group_id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def display_name(self) -> str:
        return self.name or self.type.default_name
