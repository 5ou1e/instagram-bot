import logging
from uuid import UUID

from src.application.common.types import AccountStringFormat
from src.application.features.working_group.account_worker.converters.worker_create_dto_to_entities import (
    convert_worker_create_dto_to_entity,
)
from src.application.features.working_group.account_worker.converters.worker_string_converter import (
    extract_worker_create_dto_from_string,
)
from src.domain.aggregates.account.entities.account import Account
from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.aggregates.android_device_hardware.entities.android_device_hardware import (
    AndroidDeviceHardware,
)
from src.domain.aggregates.account_worker.repositories.android_device import (
    AndroidDeviceRepository,
)
from src.domain.aggregates.android_device_hardware.repositories.android_device_hardware import (
    AndroidDeviceHardwareRepository,
)
from src.domain.aggregates.proxy.entities import Proxy
from src.domain.aggregates.proxy.repository import ProxyRepository
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)


CreateWorkingGroupWorkersCommandCommandResult = type(None)


class CreateWorkingGroupWorkersCommandHandler:
    """Создать воркеров в рабочей группе"""

    def __init__(
        self,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
        account_worker_repository: AccountWorkerRepository,
        account_repository: AccountRepository,
        proxy_repository: ProxyRepository,
        android_device_repository: AndroidDeviceRepository,
        android_device_hardware_repository: AndroidDeviceHardwareRepository,
    ):
        self._uow = uow
        self._working_group_repository = working_group_repository
        self._account_worker_repository = account_worker_repository
        self._account_repository = account_repository
        self._proxy_repository = proxy_repository
        self._android_device_repository = android_device_repository
        self._android_device_hardware_repository = android_device_hardware_repository

    async def __call__(
        self,
        working_group_id: UUID,
        format_: AccountStringFormat,
        account_worker_strings: list[str],
    ) -> CreateWorkingGroupWorkersCommandCommandResult:
        async with self._uow:
            working_group = await self._working_group_repository.get_by_id(
                working_group_id
            )

            # 2. Парсим строки в DTO
            account_worker_dtos = [
                extract_worker_create_dto_from_string(string=s, format_=format_)
                for s in account_worker_strings
            ]

            # 3. Конвертируем DTO в сущности (dict с account_worker, account, proxy, android_device_hardware)
            workers_data = [
                convert_worker_create_dto_to_entity(
                    dto=dto, working_group_id=working_group_id
                )
                for dto in account_worker_dtos
            ]

            # 4. Сохраняем все вложенные объекты и самих воркеров
            await self._create_workers(workers_data)

    async def _create_workers(self, workers_data: list[dict]):
        # Собираем вложенные объекты
        accounts = [w["account"] for w in workers_data]
        proxies = [w["proxy"] for w in workers_data if w["proxy"]]
        devices = [
            w["android_device_hardware"]
            for w in workers_data
            if w["android_device_hardware"]
        ]
        workers = [w["account_worker"] for w in workers_data]

        # 1. Proxies
        all_proxies = await self._create_proxies(proxies)

        # 2. AndroidDeviceHardwares
        hardwares = [d.hardware for d in devices if d and d.hardware]
        all_hardwares = await self._create_android_device_hardwares(hardwares)

        # 3. AndroidDevices
        hardwares_map = {h.unique_key: h for h in all_hardwares}
        print(hardwares_map)

        for d in devices:
            if d.hardware:
                print(d.hardware.unique_key)
                print(hardwares_map[d.hardware.unique_key])
                d.hardware = hardwares_map[d.hardware.unique_key]

        all_devices = await self._create_android_devices(devices)
        device_map = {d.id: d for d in all_devices}

        # 4. Accounts
        all_accounts = await self._create_accounts(accounts)
        account_map = {a.username: a for a in all_accounts}

        # 5. Маппим ссылки в воркерах
        for w_data in workers_data:
            worker = w_data["account_worker"]

            # аккаунт
            worker.account_id = account_map[w_data["account"].username].id

            # proxy
            print(all_proxies)
            if w_data["proxy"]:
                proxy_map = {p.unique_key: p for p in all_proxies}

                for worker in workers:
                    if worker.proxy:
                        worker.proxy = proxy_map[worker.proxy.unique_key]

            # android device
            if w_data["android_device_hardware"]:
                worker.android_device = device_map.get(
                    w_data["android_device_hardware"].id
                )

        print(workers)

        # 6. Workers
        await self._account_worker_repository.bulk_create(
            workers, on_conflict_do_nothing=True
        )

    async def _create_android_device_hardwares(
        self, hardwares: list[AndroidDeviceHardware]
    ):
        await self._android_device_hardware_repository.bulk_create(
            hardwares,
            on_conflict_do_nothing=True,
        )

        unique_keys = [hardware.unique_key for hardware in hardwares]
        return await self._android_device_hardware_repository.get_by_unique_keys(
            unique_keys=unique_keys
        )

    async def _create_android_devices(self, devices):
        await self._android_device_repository.bulk_create(
            devices,
            on_conflict_do_nothing=True,
        )

        device_ids = [d.id for d in devices if d.id]
        return await self._android_device_repository.get(device_ids=device_ids)

    async def _create_accounts(self, accounts: list[Account]) -> list[Account]:
        await self._account_repository.bulk_create(
            accounts,
            on_conflict_do_nothing=True,
        )
        usernames = [a.username for a in accounts]
        return await self._account_repository.get_by_usernames(usernames)

    async def _create_proxies(self, proxies: list[Proxy]) -> list[Proxy]:

        await self._proxy_repository.bulk_create(
            proxies,
            on_conflict_do_nothing=True,
        )

        return await self._proxy_repository.get_by_unique_keys(
            [p.unique_key for p in proxies]
        )
