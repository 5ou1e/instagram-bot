import logging
from typing import TypeVar

from aiograpi import Client as AiograpiClient
from aiohttp import ClientSession, ClientTimeout

from src.domain.aggregates.account.entities.account import Account
from src.domain.aggregates.account_worker.entities.account_worker_log import (
    AccountWorkerLogType,
)
from src.domain.shared.interfaces.instagram import InstagramNetworkConfig
from src.domain.shared.interfaces.instagram.web_client.builder import (
    WebInstagramClientBuilder,
)
from src.domain.shared.interfaces.instagram.web_client.client import WebInstagramClient
from src.domain.shared.interfaces.instagram.web_client.config import (
    WebInstagramClientConfig,
)
from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.account_worker_logger import PostgresAccountWorkerLogger
from src.infrastructure.instagram.web_client import WebInstagramClientImpl
from src.infrastructure.instagram.web_client.apis.graphql_api.api import (
    InstagramGraphQL,
)
from src.infrastructure.instagram.web_client.apis.wep_api.api import InstagramWebAPI

TApi = TypeVar("TApi")  # Тип API клиента

python_logger = logging.getLogger(__name__)


class WebInstagramClientBuilderImpl(WebInstagramClientBuilder):

    def build(
        self,
        account: Account,
        logger: Logger,
        network_config: InstagramNetworkConfig,
    ) -> WebInstagramClient:

        config = WebInstagramClientConfig(
            proxy=account.proxy,
            user_agent=account.user_agent,
            user_agent_mobile=account.user_agent_mobile,
            cookies=account.cookies,
        )

        timeout = ClientTimeout(total=network_config.max_network_wait_time)
        session = ClientSession(timeout=timeout)

        client_logger = PostgresAccountWorkerLogger(
            queue=logger._queue,
            account_id=logger._account_id,
            logs_type=AccountWorkerLogType.INSTAGRAM_CLIENT,
        )
        client_logger._seq_number = logger._seq_number

        web_api = InstagramWebAPI(
            session,
            config,
            client_logger,
            max_retries_on_network_errors=network_config.max_retries_on_network_errors,
            delay_before_retries_on_network_errors=network_config.delay_before_retries_on_network_errors,
        )
        graphql_api = InstagramGraphQL(
            session,
            config,
            client_logger,
            max_retries_on_network_errors=network_config.max_retries_on_network_errors,
            delay_before_retries_on_network_errors=network_config.delay_before_retries_on_network_errors,
        )

        aiograpi = AiograpiClient(proxy=account.proxy.url)

        return WebInstagramClientImpl(
            session,
            web_api,
            graphql_api,
            aiograpi,
            config,
            logger,
        )
