from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field

from src.domain.working_group.entities.worker_task.base import AccountWorkerTaskType


class UpdateWorkingGroupAccountWorkerTaskData(BaseModel):
    name: Optional[str] = None
    enabled: Optional[bool] = None
    index: Optional[int] = None
    config: Optional[dict] = None


class AuthorizeConfigData(BaseModel):
    pass


class ResetPasswordConfigData(BaseModel):
    pass


class ActionsWithUsersConfigData(BaseModel):
    pass


class DoTasksFromBoostServicesConfigData(BaseModel):
    pass


class BaseCreateWorkingGroupAccountWorkerTaskData(BaseModel):
    name: Optional[str] = None
    enabled: Optional[bool] = False
    index: Optional[int] = None


class CreateAuthorizeWorkingGroupAccountWorkerTaskData(
    BaseCreateWorkingGroupAccountWorkerTaskData
):
    type: Literal[AccountWorkerTaskType.AUTHORIZE_ACCOUNT.value]
    config: AuthorizeConfigData | None = None
    enabled: bool = False


class CreateResetPasswordWorkingGroupAccountWorkerTaskData(
    BaseCreateWorkingGroupAccountWorkerTaskData
):
    type: Literal[AccountWorkerTaskType.RESET_PASSWORD_BY_EMAIL.value]
    config: ResetPasswordConfigData | None = None
    enabled: bool = False


class CreateActionsWithUsersWorkingGroupAccountWorkerTaskData(
    BaseCreateWorkingGroupAccountWorkerTaskData
):
    type: Literal[AccountWorkerTaskType.ACTIONS_WITH_USERS.value]
    config: ActionsWithUsersConfigData | None = None
    enabled: bool = False


class CreateDoTasksFromBoostServicesWorkingGroupAccountWorkerTaskData(
    BaseCreateWorkingGroupAccountWorkerTaskData
):
    type: Literal[AccountWorkerTaskType.DO_TASKS_FROM_BOOST_SERVICES.value]
    config: DoTasksFromBoostServicesConfigData | None = None
    enabled: bool = False


CreateSubtaskData = Union[
    CreateAuthorizeWorkingGroupAccountWorkerTaskData,
    CreateResetPasswordWorkingGroupAccountWorkerTaskData,
    CreateActionsWithUsersWorkingGroupAccountWorkerTaskData,
    CreateDoTasksFromBoostServicesWorkingGroupAccountWorkerTaskData,
]


class CreateWorkingGroupAccountWorkerTaskData(BaseModel):
    """Данные для создания задачи для аккаунтов"""

    type: AccountWorkerTaskType

    # Опциональные поля
    name: Optional[str] = None
    enabled: bool = False
    index: int | None = None
    config: dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True
        extra = "forbid"
