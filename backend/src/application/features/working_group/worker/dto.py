from dataclasses import dataclass
from typing import Literal, Optional

from src.application.common.dtos.account_worker import AccountWorkerDTO
from src.application.common.dtos.pagination import PaginationResult
from src.domain.shared.interfaces.instagram.version import InstagramAppVersion


@dataclass
class AccountWorkerCreateAccountDTO:
    username: str
    password: str
    email_username: Optional[str]
    email_password: Optional[str]
    user_id: Optional[int]
    follow_actions_count: int


@dataclass
class AccountWorkerCreateProxyDTO:
    raw_proxy_string: str


@dataclass
class AccountWorkerCreateAndroidDeviceHardwareDTO:
    manufacturer: str
    brand: str
    model: str
    device: str
    cpu: str
    dpi: str
    resolution: str
    os_version: str
    os_api_level: str


@dataclass
class AccountWorkerCreateAndroidDeviceDTO:
    hardware: Optional[AccountWorkerCreateAndroidDeviceHardwareDTO]
    os_version: str
    os_api_level: str
    locale: str
    timezone: str
    connection_type: Literal["WIFI", "MOBILE(LTE)"]
    instagram_app_version: InstagramAppVersion
    instagram_app_data: dict  # сюда можно класть InstagramAppDataDTO


@dataclass
class AccountWorkerCreateDTO:
    account: AccountWorkerCreateAccountDTO
    proxy: Optional[AccountWorkerCreateProxyDTO]
    android_device: Optional[AccountWorkerCreateAndroidDeviceDTO]


@dataclass
class WorkingGroupWorkersDTO:
    workers: list[AccountWorkerDTO]
    pagination: PaginationResult
