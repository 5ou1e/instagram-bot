from dataclasses import dataclass

from src.domain.aggregates.account_worker.entities.account_worker.entity import (
    AccountWorker,
)
from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.aggregates.proxy.entities import Proxy
from src.domain.aggregates.proxy.exceptions import NoAvailableProxyError
from src.domain.services.worker_workflow.providers.proxy_provider import ProxyProvider
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.utils import current_datetime


@dataclass
class ChangeProxyActionContext:
    logger: Logger
    uow: Uow
    proxy_provider: ProxyProvider
    account_worker_repository: AccountWorkerRepository


class AccountWorkerChangeProxyActionExecutor:
    def __init__(self, ctx: ChangeProxyActionContext):
        self.ctx = ctx
        self.logger = ctx.logger

    async def __call__(
        self,
        worker: AccountWorker,
    ):
        await self.logger.info(f"Меняю прокси")
        await self._release_worker_proxy(worker)
        new_proxy = await self._wait_for_available_proxy()
        await self._set_worker_new_proxy(worker, new_proxy)
        await self.logger.info("Поменял прокси на: %s", new_proxy.url)

    async def _release_worker_proxy(self, worker: AccountWorker):
        if worker.proxy:
            await self.ctx.proxy_provider.release(worker.proxy)
            async with self.ctx.uow:
                worker.set_proxy(None)
                await self.ctx.account_worker_repository.update(worker)

    async def _wait_for_available_proxy(self) -> Proxy:
        try:
            return await self.ctx.proxy_provider.acquire()
        except NoAvailableProxyError:
            await self.ctx.logger.info("Нету доступного прокси")
            raise

    async def _set_worker_new_proxy(self, worker: AccountWorker, proxy: Proxy):
        async with self.ctx.uow:
            worker.set_proxy(proxy)
            worker.last_action_time = current_datetime()
            await self.ctx.account_worker_repository.update(worker)
