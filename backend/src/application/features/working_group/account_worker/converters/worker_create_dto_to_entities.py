from uuid import UUID

from uuid6 import uuid7

from src.application.common.converters.proxy import convert_proxy_line_to_entity
from src.application.features.working_group.account_worker.dto import (
    AccountWorkerCreateAccountDTO,
    AccountWorkerCreateAndroidDeviceDTO,
    AccountWorkerCreateDTO,
    AccountWorkerCreateProxyDTO,
)
from src.domain.aggregates.account.entities.account import (
    Account,
    AccountActionStatistics, Email,
)
from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.aggregates.account_worker.entities.android_device import AndroidDevice

from src.domain.aggregates.android_device_hardware.entities.android_device_hardware import (
    AndroidDeviceHardware,
)
from src.domain.aggregates.proxy.entities import Proxy


def map_account(dto: AccountWorkerCreateAccountDTO) -> Account:
    email = None
    if dto.email_username and dto.email_password:
        email = Email(username=dto.email_username, password=dto.email_password)

    return Account(
        id=uuid7(),
        username=dto.username,
        password=dto.password,
        email=email,
        user_id=dto.user_id,
        action_statistics=AccountActionStatistics(follows=dto.follow_actions_count),
    )


def map_proxy(dto: AccountWorkerCreateProxyDTO | None) -> Proxy | None:
    if not dto:
        return None

    return convert_proxy_line_to_entity(dto.raw_proxy_string)


def map_android_device(
    dto: AccountWorkerCreateAndroidDeviceDTO | None,
) -> AndroidDevice | None:
    if not dto:
        return None

    hardware = None

    if dto.hardware:

        hardware = AndroidDeviceHardware(
            id=uuid7(),
            name=dto.hardware.manufacturer + "/" + dto.hardware.brand,
            manufacturer=dto.hardware.manufacturer,
            brand=dto.hardware.brand,
            model=dto.hardware.model,
            device=dto.hardware.device,
            cpu=dto.hardware.cpu,
            dpi=dto.hardware.dpi,
            resolution=dto.hardware.resolution,
            os_version=dto.hardware.os_version,
            os_api_level=dto.hardware.os_api_level,
        )

    # instagram_app_data у тебя DTO (dict), можно замаппить на entity:
    app_data = dto.instagram_app_data

    return AndroidDevice(
        id=uuid7(),
        hardware=hardware,
        os_version=dto.os_version,
        os_api_level=dto.os_api_level,
        locale=dto.locale,
        timezone=dto.timezone,
        connection_type=dto.connection_type,
        instagram_app_version=dto.instagram_app_version,
        instagram_app_data=app_data,
    )


def convert_worker_create_dto_to_entity(
    dto: AccountWorkerCreateDTO, working_group_id: UUID
) -> dict:
    account = map_account(dto.account)
    proxy = map_proxy(dto.proxy)
    android_device = map_android_device(dto.android_device)
    worker = AccountWorker(
        id=uuid7(),
        working_group_id=working_group_id,
        account_id=account.id,
        android_device=android_device,
        proxy=proxy,
    )

    return {
        "account_worker": worker,
        "account": account,
        "proxy": proxy,
        "android_device_hardware": android_device,
    }
