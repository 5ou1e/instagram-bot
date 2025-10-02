import asyncio
from typing import Awaitable, Callable, TypeVar

from src.domain.shared.interfaces.instagram.exceptions import NetworkError
from src.domain.shared.interfaces.instagram.mobile_client.client import (
    MobileInstagramClient,
)
from src.domain.shared.interfaces.instagram.mobile_client.converters import (
    sync_android_device_instagram_app_data_from_client_local_data,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.account_worker.repositories.account_worker import AccountWorkerRepository
from src.domain.account_worker.services.actions_old.change_proxy import (
    ChangeProxyActionContext,
    AccountWorkerChangeProxyActionExecutor,
)
from src.domain.account_worker.services.providers.proxy_provider import ProxyProvider

T = TypeVar("T")


class InstagramActionWrapper:
    def __init__(
        self,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,
        proxy_provider: ProxyProvider,
        logger: Logger,
        max_proxy_changes: int = 3,
        delay_before_proxy_change: int = 5,
    ):
        self._uow = uow
        self._account_worker_repository = account_worker_repository
        self._proxy_provider = proxy_provider
        self._logger = logger
        self._max_proxy_changes = max_proxy_changes
        self._delay_before_proxy_change = delay_before_proxy_change

    async def execute(
        self,
        handler: Callable[..., Awaitable[T]],
        worker: AccountWorker,
        client: MobileInstagramClient,
        *args,
        **kwargs,
    ) -> T:
        """
        Выполняет действие в Instagram с ротацией прокси при NetworkError и сохранением куки.
        """
        errors = 0
        network_error_occurred = False

        while True:
            try:
                result = await handler(*args, **kwargs)
                network_error_occurred = False
                return result

            except NetworkError as e:
                raise e
                network_error_occurred = True
                errors += 1

                if not self._max_proxy_changes or errors > self._max_proxy_changes:
                    raise

                await self._logger.info(
                    "Ошибка соединения, меняем прокси %s/%s: %s",
                    errors,
                    self._max_proxy_changes,
                    e,
                )

                await asyncio.sleep(self._delay_before_proxy_change)

                await self._change_proxy(worker)
                client.set_proxy(worker.proxy)

            finally:
                if not network_error_occurred:
                    await self._sync_and_save_instagram_local_data(worker, client)

    async def _change_proxy(self, worker: AccountWorker) -> None:
        action = AccountWorkerChangeProxyActionExecutor(
            ChangeProxyActionContext(
                uow=self._uow,
                logger=self._logger,
                account_worker_repository=self._account_worker_repository,
                proxy_provider=self._proxy_provider,
            )
        )
        await action(worker)

    async def _sync_and_save_instagram_local_data(
        self,
        worker: AccountWorker,
        client: MobileInstagramClient,
    ) -> None:
        async with self._uow:
            sync_android_device_instagram_app_data_from_client_local_data(
                worker.android_device, client
            )
            await self._account_worker_repository.update(worker)
