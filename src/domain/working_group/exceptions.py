from dataclasses import dataclass
from uuid import UUID

from src.domain.shared.exceptions import DomainError


@dataclass(kw_only=True, slots=True)
class WorkingGroupNameAlreadyExistsError(DomainError):

    @property
    def title(self) -> str:
        return f"Рабочая группа с таким именем уже существует"


@dataclass(kw_only=True, slots=True)
class WorkingGroupIdDoesNotExistError(DomainError):
    working_group_id: UUID

    @property
    def title(self) -> str:
        return f"Рабочей группы с ID: {self.working_group_id} не существует"


@dataclass(kw_only=True, slots=True)
class WorkingGroupCannotBeStartedError(DomainError):
    working_group_id: UUID

    @property
    def title(self) -> str:
        return (
            f"Рабочая группа не может быть запущена, т.к в находится другом состоянии"
        )


@dataclass(kw_only=True, slots=True)
class WorkingGroupCannotBeStopedError(DomainError):
    working_group_id: UUID

    @property
    def title(self) -> str:
        return f"Рабочая группа не может быть остановлена, т.к в находится другом состоянии"


@dataclass(kw_only=True, slots=True)
class WorkingGroupDoesNotHaveEnabledSubtasksError(DomainError):

    @property
    def title(self) -> str:
        return f"Сначала включите задачи для аккаунтов-воркеров"


@dataclass(kw_only=True, slots=True)
class WorkingGroupProcessingAccountsCountExceededError(DomainError):

    @property
    def title(self) -> str:
        return f"Превышен лимит работающих воркеров рабочей группы"


@dataclass(kw_only=True, slots=True)
class WorkingGroupIsNotWorkingError(DomainError):

    @property
    def title(self) -> str:
        return f"Рабочая группа не в состоянии WORKING"


@dataclass(kw_only=True, slots=True)
class WorkingGroupWithThisNameAlreadyExistError(DomainError):
    name: str

    @property
    def title(self) -> str:
        return f"Рабочая группа с именем «{self.name}» уже существует"


@dataclass(kw_only=True, slots=True)
class WorkerTaskIdDoesNotExistError(DomainError):
    task_id: UUID

    @property
    def title(self) -> str:
        return f"Задачи с ID: {self.task_id} не существует"


@dataclass(kw_only=True, slots=True)
class WorkerTaskNameAlreadyExistsError(DomainError):
    name: str

    @property
    def title(self) -> str:
        return f"Задача для аккаунтов с именем {self.name} уже существует"


@dataclass(kw_only=True, slots=True)
class AccountDoesNotHaveEmailError(DomainError):
    @property
    def title(self):
        return "У аккаунта не указан E-mail"


@dataclass(kw_only=True, slots=True)
class AccountWorkerIdDoesNotExistError(DomainError):
    account_worker_id: UUID

    @property
    def title(self) -> str:
        return f"Аккаунт-воркера с ID: {self.account_worker_id} не существует"


@dataclass(kw_only=True, slots=True)
class WorkerAlreadyWorkedWithinLastWorkingGroupExecutionError(DomainError):

    @property
    def title(self) -> str:
        return (
            f"Аккаунт-воркер уже запускался в рамках последнего запуска рабочей группы"
        )


@dataclass(kw_only=True, slots=True)
class AccountDoesNotHaveSessionIdError(DomainError):

    @property
    def title(self) -> str:
        return f"Отсутствует sessionid"


@dataclass(kw_only=True, slots=True)
class WorkingGroupAccountWorkerTaskIdDoesNotExistError(DomainError):
    working_group_id: UUID
    task_id: UUID

    @property
    def title(self) -> str:
        return f"Задача для аккаунтов с ID {self.task_id} не существует в рабочей группе ID {self.working_group_id}"
