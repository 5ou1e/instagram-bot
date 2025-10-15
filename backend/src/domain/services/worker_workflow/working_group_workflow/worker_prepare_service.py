from uuid6 import uuid7

from src.application.features.working_group.account_worker.converters.iam_mob import (
    extract_ig_app_version_from_ig_android_user_agent,
    extract_locale_from_ig_android_user_agent,
)
from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.aggregates.account_worker.entities.android_device import AndroidDevice, \
    AndroidDeviceInstagramAppData

from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)

from src.domain.aggregates.android_device_hardware.repositories.android_device_hardware import (
    AndroidDeviceHardwareRepository,
)
from src.domain.aggregates.proxy.exceptions import NoAvailableProxyError
from src.domain.services.worker_workflow.providers.proxy_provider import ProxyProvider
from src.domain.shared.interfaces.logger import AccountWorkerLogger
from src.domain.shared.interfaces.uow import Uow


class AccountWorkerPrepareBeforeWorkService:
    """Выполняет подготовку аккаунт-воркера перед работой - установку прокси/девайса"""

    def __init__(
        self,
        uow: Uow,
        proxy_provider: ProxyProvider,
        android_device_hardware_repository: AndroidDeviceHardwareRepository,
        account_worker_repository: AccountWorkerRepository,
        worker_logger: AccountWorkerLogger,
    ):
        self._uow = uow
        self._proxy_provider = proxy_provider
        self._android_device_hardware_repository = android_device_hardware_repository
        self._account_worker_repository = account_worker_repository
        self._worker_logger = worker_logger

    async def prepare(self, worker: AccountWorker):
        await self._ensure_android_device(worker)
        # await self._ensure_proxy(account_worker)

    async def _ensure_android_device(
        self,
        worker: AccountWorker,
    ):
        # TODO рефакторинг
        if not worker.android_device:

            hardwares = await self._android_device_hardware_repository.get_all()
            android_hardware = hardwares[0]

            ua = "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)"
            instagram_app_version = extract_ig_app_version_from_ig_android_user_agent(
                ua
            )
            locale = extract_locale_from_ig_android_user_agent(ua) or "en_US"

            worker.set_android_device(
                AndroidDevice(
                    id=uuid7(),
                    hardware=android_hardware,
                    locale=locale,
                    instagram_app_version=instagram_app_version,
                    instagram_app_data=AndroidDeviceInstagramAppData.create(),
                    os_version="15",
                    os_api_level="35",
                )
            )

            await self._worker_logger.info(
                f"Установил новый андроид-девайс: {worker.android_device}"
            )
            async with self._uow:
                await self._account_worker_repository.update(worker)

        if not worker.android_device.hardware:

            hardwares = await self._android_device_hardware_repository.get_all()
            android_hardware = hardwares[0]

            worker.set_android_device_hardware(android_hardware)
            await self._worker_logger.info(
                f"Установил новые параметры железа для девайса: {worker.android_device}"
            )
            async with self._uow:
                await self._account_worker_repository.update(worker)
        else:
            await self._worker_logger.info(
                f"Работаю через андроид-девайс: {worker.android_device}"
            )

    async def _ensure_proxy(self, worker: AccountWorker):

        if not worker.proxy:

            while True:
                proxy = await self._proxy_provider.acquire()
                if not proxy:
                    await self._worker_logger.info("Нету доступного прокси")
                    raise NoAvailableProxyError()
                    # await asyncio.sleep(5)
                    # continue
                worker.set_proxy(proxy)

                async with self._uow:
                    await self._account_worker_repository.update(worker)
                await self._worker_logger.info(f"Взял новый прокси: {proxy}")

                return
        else:
            await self._worker_logger.info(
                f"Работаю с прокси: {worker.proxy.url if worker.proxy else None}"
            )
