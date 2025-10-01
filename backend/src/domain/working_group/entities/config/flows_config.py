from pydantic import BaseModel, Field


class WorkingGroupUnauthorizedFlowConfig(BaseModel):
    handle_challenges: bool = Field(
        default=True,
        title="Обработка челленджей",
        description="Обрабатывать челленджи в неавторизованном состоянии",
    )


class WorkingGroupAuthorizedFlowConfig(BaseModel):
    handle_challenges: bool = Field(
        default=True,
        title="Обработка челленджей",
        description="Обрабатывать челленджи в авторизованном состоянии",
    )
    reauthorize_on_unauthorized: bool = Field(
        default=True,
        title="Переавторизация",
        description="Переавторизоваться при потере авторизации",
    )


class WorkingGroupAuthorizationFlowConfig(BaseModel):
    handle_challenges: bool = Field(
        default=True,
        title="Обработка челленджей",
        description="Обрабатывать челленджи при авторизации",
    )
    on_bad_password_change_password_by_email: bool = Field(
        default=False,
        title="При неверном пароле восстанавливать его через почту",
        description="При неверном пароле восстанавливать его через почту",
    )


class WorkingGroupFlowsConfig(BaseModel):
    authorization: WorkingGroupAuthorizationFlowConfig = Field(
        default_factory=WorkingGroupAuthorizationFlowConfig,
        title="Настройки авторизации",
        description="Настройки процесса авторизации",
    )
    authorized: WorkingGroupAuthorizedFlowConfig = Field(
        default_factory=WorkingGroupAuthorizedFlowConfig,
        title="Настройки авторизованного режима",
        description="Настройки работы в авторизованном состоянии",
    )
    unauthorized: WorkingGroupUnauthorizedFlowConfig = Field(
        default_factory=WorkingGroupUnauthorizedFlowConfig,
        title="Настройки неавторизованного режима",
        description="Настройки работы в неавторизованном состоянии",
    )
