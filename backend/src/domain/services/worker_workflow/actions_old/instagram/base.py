from dataclasses import dataclass, field
from typing import Generic, Tuple, Type, TypeVar

from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker

from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.services.worker_workflow.actions_old.instagram.instagram_action_wrapper import (
    InstagramActionWrapper,
)
from src.domain.services.worker_workflow.providers.proxy_provider import ProxyProvider
from src.domain.shared.exceptions import DomainError
from src.domain.shared.interfaces.instagram.exceptions import NetworkError
from src.domain.shared.interfaces.instagram.instagram_network_config import (
    InstagramNetworkConfig,
)
from src.domain.shared.interfaces.instagram.mobile_client.client import (
    MobileInstagramClient,
)
from src.domain.shared.interfaces.instagram.mobile_client.config import (
    MobileInstagramClientNetworkConfig,
)
from src.domain.shared.interfaces.instagram.mobile_client.converters import (
    mobile_client_device_info_from_android_device,
    mobile_client_local_data_from_android_device_app_data,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.infrastructure.instagram import MobileInstagramClientBuilderImpl


@dataclass
class FlowConfig:
    """Базовая конфигурация всех Flows"""

    # Retry настройки
    max_attempts: int = 1
    retry_delay: float = 0.0

    # Какие ошибки ретраить
    retryable_exceptions: Tuple[Type[Exception], ...] = field(
        default_factory=lambda: (DomainError, NetworkError)
    )

    handle_challenges: bool = True

    instagram_network_config: InstagramNetworkConfig = field(
        default_factory=InstagramNetworkConfig
    )


@dataclass(kw_only=True)
class FlowContext:
    """Базовый контекст для всех Flows"""

    account_repository: AccountRepository
    account_worker_repository: AccountWorkerRepository
    proxy_provider: ProxyProvider
    uow: Uow
    logger: Logger


TContext = TypeVar("TContext", bound=FlowContext)

TConfig = TypeVar("TConfig", bound=FlowConfig)


class Flow(Generic[TContext, TConfig]):
    """
    Базовый класс для всех Flows
    """

    def __init__(self, ctx: TContext, config: TConfig):
        self._ctx = ctx
        self._config = config
        self._logger = ctx.logger

        self._ig_action_wrapper: InstagramActionWrapper = InstagramActionWrapper(
            uow=self._ctx.uow,
            account_worker_repository=self._ctx.account_worker_repository,
            proxy_provider=self._ctx.proxy_provider,
            logger=self._ctx.logger,
            max_proxy_changes=self._config.instagram_network_config.max_proxy_changes_on_network_errors,
            delay_before_proxy_change=self._config.instagram_network_config.delay_before_proxy_changes_on_network_errors,
        )

    def _build_instagram_client(
        self,
        worker: AccountWorker,
    ) -> MobileInstagramClient:
        local_data = mobile_client_local_data_from_android_device_app_data(
            worker.android_device.instagram_app_data
        )
        device_info = mobile_client_device_info_from_android_device(
            worker.android_device
        )

        return (
            MobileInstagramClientBuilderImpl.new()
            .with_device_info(device_info)
            .with_local_data(local_data)
            .with_network_config(
                MobileInstagramClientNetworkConfig(
                    proxy=worker.proxy,
                    max_network_wait_time=20,
                    max_retries_on_network_errors=0,
                    delay_before_retries_on_network_errors=0,
                )
            )
            .with_logger(self._logger)
            .build()
        )
