import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from mashumaro import DataClassDictMixin

from src.domain.android_device_hardware.entities.android_device import AndroidDeviceInstagramAppData
from src.domain.shared.interfaces.instagram.version import InstagramAppVersion
from src.domain.account_worker.entities.account_worker.work_state import AccountWorkerWorkState


@dataclass(kw_only=True, slots=True)
class AndroidDeviceHardwareDTO:
    id: uuid.UUID
    name: str  # "Xiaomi Redmi Note 8"
    manufacturer: str  # "Xiaomi"
    brand: str  # "xiaomi"
    model: str  # "Redmi Note 8"
    device: str  # "ginkgo"
    cpu: str  # "qcom"
    dpi: str  # "440"
    resolution: str  # "1080x2130"
    os_version: str  # "10"
    os_api_level: str  # "29"


@dataclass(kw_only=True, slots=True)
class AndroidDeviceDTO:
    id: uuid.UUID
    hardware: AndroidDeviceHardwareDTO | None = None

    # Переопределяем заводские настройки ОС
    os_version: str = None
    os_api_level: str = None

    locale: str
    timezone: str
    connection_type: Literal["WIFI", "MOBILE(LTE)"]

    instagram_app_version: InstagramAppVersion = InstagramAppVersion.V374
    instagram_app_data: AndroidDeviceInstagramAppData


@dataclass(kw_only=True, slots=True)
class AccountActionStatisticsDTO(DataClassDictMixin):
    follows: int = 0
    follows_blocks: int = 0
    authorizations: int = 0


@dataclass(kw_only=True, slots=True)
class AccountWorkerDTO:
    id: UUID
    account_id: UUID
    working_group_id: UUID
    username: str
    password: str | None = None
    email_username: str | None = None
    email_password: str | None = None
    proxy: str | None = None
    action_statistics: AccountActionStatisticsDTO
    status: str | None = None
    last_log_message: str | None = None
    last_action_time: datetime | None = None
    password_changed_datetime: datetime | None = None
    created_at: datetime | None = None
    attached_to_task: datetime | None = None
    android_device: AndroidDeviceDTO | None = None
    work_state: AccountWorkerWorkState | None = None
