from typing import Optional

from pydantic import BaseModel, Field

from src.domain.account.entities.account_log import AccountWorkerLogLevel


# === AccountOnStartWorkConfigPatch ===
class WorkingGroupAccountOnStartWorkConfigPatch(BaseModel):
    ensure_session_is_valid: Optional[bool] = None
    authorize_by_login_and_password_if_session_is_invalid: Optional[bool] = None


# === AuthorizationFlowConfigPatch ===
class WorkingGroupAuthorizationFlowConfigPatch(BaseModel):
    handle_challenges: Optional[bool] = None
    on_bad_password_change_password_by_email: Optional[bool] = None


# === AuthorizedFlowConfigPatch ===
class WorkingGroupAuthorizedFlowConfigPatch(BaseModel):
    handle_challenges: Optional[bool] = None
    reauthorize_on_unauthorized: Optional[bool] = None


# === UnauthorizedFlowConfigPatch ===
class WorkingGroupUnauthorizedFlowConfigPatch(BaseModel):
    handle_challenges: Optional[bool] = None


# === FlowsConfigPatch ===
class WorkingGroupFlowsConfigPatch(BaseModel):
    authorization: Optional[WorkingGroupAuthorizationFlowConfigPatch] = None
    authorized: Optional[WorkingGroupAuthorizedFlowConfigPatch] = None
    unauthorized: Optional[WorkingGroupUnauthorizedFlowConfigPatch] = None


# === GeneralConfigPatch ===
class WorkingGroupGeneralConfigPatch(BaseModel):
    max_parallel_processing_accounts_count: Optional[int] = Field(
        default=None,
        ge=1,
        le=1000,
        description="Макс. одновременно работающих аккаунтов",
    )
    delay_before_start_new_account: Optional[int] = Field(
        default=None,
        ge=0,
        le=300,
        description="Задержка в секундах перед запуском нового аккаунта",
    )
    wait_for_new_accounts_if_all_processed: Optional[bool] = None


# === NetworkConfigPatch ===
class WorkingGroupNetworkConfigPatch(BaseModel):
    max_network_wait_time: Optional[int] = Field(
        default=None,
        ge=5,
        le=120,
        description="Максимальное время ожидания сетевого запроса в секундах",
    )
    retry_on_network_errors: Optional[bool] = None
    max_retries_on_network_errors: Optional[int] = Field(
        default=None,
        ge=0,
        le=10,
        description="Максимальное количество повторных попыток при сетевых ошибках",
    )
    delay_before_retries_on_network_errors: Optional[int] = Field(
        default=None,
        ge=0,
        le=60,
        description="Задержка в секундах перед повторной попыткой при сетевой ошибке",
    )
    work_with_proxy: Optional[bool] = None
    max_accounts_per_proxy: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
        description="Максимальное количество аккаунтов на один прокси",
    )
    change_proxy_on_network_errors: Optional[bool] = None
    max_proxy_changes_on_network_errors: Optional[int] = Field(
        default=None,
        ge=0,
        le=10,
        description="Максимальное количество смен прокси при сетевых ошибках",
    )
    delay_before_proxy_changes_on_network_errors: Optional[int] = Field(
        default=None,
        ge=0,
        le=30,
        description="Задержка в секундах перед сменой прокси при ошибке",
    )


# === LoggingConfigPatch ===
class WorkingGroupLoggingConfigPatch(BaseModel):
    enabled: Optional[bool] = None
    level: Optional[AccountWorkerLogLevel] = None


# === Root WorkingGroupConfig Patch ===
class WorkingGroupConfigPatch(BaseModel):
    general: Optional[WorkingGroupGeneralConfigPatch] = None
    network: Optional[WorkingGroupNetworkConfigPatch] = None
    logging: Optional[WorkingGroupLoggingConfigPatch] = None
    flows: Optional[WorkingGroupFlowsConfigPatch] = None
    account_on_start_work: Optional[WorkingGroupAccountOnStartWorkConfigPatch] = None

    class Config:
        extra = "forbid"
