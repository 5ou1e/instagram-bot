from pydantic import BaseModel, Field

from src.domain.shared.interfaces.instagram.instagram_network_config import (
    InstagramNetworkConfig,
)
from src.domain.working_group.entities.config.flows_config import (
    WorkingGroupFlowsConfig,
)
from src.domain.working_group.entities.config.general_config import (
    WorkingGroupGeneralConfig,
)
from src.domain.working_group.entities.config.logging_config import (
    WorkingGroupLoggingConfig,
)
from src.domain.working_group.entities.config.network_config import (
    WorkingGroupNetworkConfig,
)


class AccountWorkerOnStartWorkConfig(BaseModel):
    ensure_session_is_valid: bool = Field(
        default=True,
        title="Проверять валидность сессии",
        description="Проверять валидность сессии при старте работы с аккаунтом",
    )
    authorize_by_login_and_password_if_session_is_invalid: bool = Field(
        default=True,
        title="Авторизоваться по логину и паролю если сессия невалидна",
        description="Авторизоваться по логину и паролю если сессия невалидна",
    )


class WorkingGroupConfig(BaseModel):
    """Настройки задачи"""

    general: WorkingGroupGeneralConfig = Field(
        default_factory=WorkingGroupGeneralConfig,
        title="Общие настройки",
        description="Общие настройки выполнения задачи",
    )
    network: WorkingGroupNetworkConfig = Field(
        default_factory=WorkingGroupNetworkConfig,
        title="Сетевые настройки",
        description="Настройки сетевого взаимодействия",
    )
    logging: WorkingGroupLoggingConfig = Field(
        default_factory=WorkingGroupLoggingConfig,
        title="Настройки логирования",
        description="Настройки системы логирования",
    )
    flows: WorkingGroupFlowsConfig = Field(
        default_factory=WorkingGroupFlowsConfig,
        title="Настройки потоков",
        description="Настройки различных режимов работы",
    )
    account_worker_on_start_work: AccountWorkerOnStartWorkConfig = Field(
        default_factory=AccountWorkerOnStartWorkConfig,
        title="Настройки старта работы",
        description="Настройки при начале работы с аккаунтом",
    )

    class Config:
        validate_assignment = True
        use_enum_values = True

    @property
    def instagram_network_config(self) -> InstagramNetworkConfig:
        """Преобразует network настройки в конфиг для Instagram Client"""

        return InstagramNetworkConfig(
            max_network_wait_time=self.network.max_network_wait_time,
            max_retries_on_network_errors=self.network.max_retries_on_network_errors,
            delay_before_retries_on_network_errors=self.network.delay_before_retries_on_network_errors,
            work_with_proxy=self.network.work_with_proxy,
            change_proxy_on_network_errors=self.network.change_proxy_on_network_errors,
            max_proxy_changes_on_network_errors=self.network.max_proxy_changes_on_network_errors,
            delay_before_proxy_changes_on_network_errors=self.network.delay_before_proxy_changes_on_network_errors,
        )
