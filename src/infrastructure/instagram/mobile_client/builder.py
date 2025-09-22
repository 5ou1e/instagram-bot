from src.domain.account.entities.account_log import AccountWorkerLogType
from src.domain.shared.interfaces.instagram.mobile_client.builder import (
    MobileInstagramClientBuilder,
)
from src.domain.shared.interfaces.instagram.mobile_client.client import (
    MobileInstagramClient,
)
from src.domain.shared.interfaces.instagram.mobile_client.config import (
    MobileInstagramClientNetworkConfig,
)
from src.domain.shared.interfaces.instagram.version import InstagramAppVersion
from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.account_worker_logger import PostgresLogger
from src.infrastructure.instagram.mobile_client.client import MobileInstagramClientImpl


class MobileInstagramClientBuilderImpl(MobileInstagramClientBuilder):

    def __init__(self):
        self.logger = None
        self.device_info = None
        self.local_data = None
        self.network_config = None
        self.proxy = None

    @classmethod
    def new(cls) -> "MobileInstagramClientBuilderImpl":
        return MobileInstagramClientBuilderImpl()

    def with_device_info(
        self,
        device_info: "MobileClientAndroidDeviceInfo",
    ) -> "MobileInstagramClientBuilderImpl":
        self.device_info = device_info
        return self

    def with_local_data(
        self,
        local_data: "MobileInstagramClientLocalData",
    ) -> "MobileInstagramClientBuilderImpl":
        self.local_data = local_data
        return self

    def with_logger(self, logger: Logger) -> "MobileInstagramClientBuilderImpl":
        self.logger = self._create_logger(logger)
        return self

    def with_network_config(
        self, network_config: MobileInstagramClientNetworkConfig
    ) -> "MobileInstagramClientBuilderImpl":
        self.network_config = network_config
        return self

    def build(
        self,
    ) -> MobileInstagramClient:
        return MobileInstagramClientImpl(
            version=InstagramAppVersion.V374,
            local_data=self.local_data,
            device_info=self.device_info,
            network_config=self.network_config,
            logger=self.logger,
        )

    def _create_logger(self, logger: PostgresLogger) -> Logger:
        """Создаем логгер клиента из логгера аккаунта"""
        instagram_logger = PostgresLogger(
            queue=logger._queue,
            account_id=logger._account_id,
            logs_type=AccountWorkerLogType.INSTAGRAM_CLIENT,
        )
        instagram_logger._seq_number = logger._seq_number

        return instagram_logger
