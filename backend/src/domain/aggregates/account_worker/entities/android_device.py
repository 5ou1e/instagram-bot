import base64
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from mashumaro import DataClassDictMixin
from orjson import orjson

from src.domain.aggregates.android_device_hardware.entities.android_device_hardware import (
    AndroidDeviceHardware,
)
from src.domain.shared.interfaces.instagram.version import InstagramAppVersion
from src.domain.shared.utils import (
    current_datetime,
    generate_android_id_from_guid,
    generate_waterfall_id,
    is_valid_uuid,
)


@dataclass(kw_only=True, slots=True)
class AndroidDevice:
    id: uuid.UUID
    hardware: AndroidDeviceHardware | None = None

    os_version: str = None
    os_api_level: str = None

    locale: str = "en_US"
    timezone: str = "Europe/Madrid"
    connection_type: Literal["WIFI", "MOBILE(LTE)"] = "WIFI"

    instagram_app_version: InstagramAppVersion = InstagramAppVersion.V374
    instagram_app_data: "AndroidDeviceInstagramAppData"

    created_at: datetime = field(default_factory=current_datetime)
    updated_at: datetime = field(default_factory=current_datetime)

    def set_hardware(self, hardware: AndroidDeviceHardware):
        self.hardware = hardware

    def set_instagram_app_version(self, instagram_app_version: InstagramAppVersion):
        self.instagram_app_version = instagram_app_version


@dataclass(kw_only=True, slots=True)
class AndroidDeviceInstagramAppData(DataClassDictMixin):
    android_id: str  # android-1923fjnma8123 ( генерируется системой, с версии android 8.0 для каждого приложения свой)
    device_id: str  # UUID v4 ( генерируется приложением ) Сбрасывается при переустановке приложения
    family_device_id: str  # UUID v4 ( генерируется приложением ) ID устройства в рамках "семьи" приложений Meta (Instagram, Facebook, WhatsApp)
    google_ad_id: str

    # Устанавливаются сервером
    authorization_data: dict = field(default_factory=dict)
    user_id: str | None = None

    # Генерируется сервером, клиент получает при первом открытии приложения /dual_keys
    mid: str | None = None
    csrf_token: str | None = None
    shbid: str | None = None
    shbts: str | None = None
    rur: str | None = None
    www_claim: str | None = None
    public_key: str | None = None  # /api/v1/launcher/mobileconfig/
    public_key_id: int | None = None  # /api/v1/launcher/mobileconfig/

    session_flush_nonce: str | None = None  # Нужна для /logout

    # UUID v4 , Генерирует клиент , меняется при каждом открытии приложения и для разных запросов тоже меняется
    waterfall_id: str = field(default_factory=generate_waterfall_id)
    # Меняется полностью при открытии\закрытии приложении и при сворачивании\разворачивании увеличивается счетчик
    pigeon_session_id: str = field(default_factory=lambda: f"UFS-{uuid.uuid4()}-0")

    # Сбрасываются при перезагрузке приложения
    requests_count: int = 0
    total_bytes: float = 0
    total_time_ms: float = 0

    @classmethod
    def create(
        cls,
        *,
        android_id: str | None = None,
        device_id: str | None = None,
        family_device_id: str | None = None,
        google_ad_id: str | None = None,
        pigeon_session_id: str | None = None,
        authorization_data: dict | None = None,
        user_id: str | None = None,
        mid: str | None = None,
        csrf_token: str | None = None,
        shbid: str | None = None,
        shbts: str | None = None,
        rur: str | None = None,
        www_claim: str | None = None,
        public_key: str | None = None,
        public_key_id: int | None = None,
        session_flush_nonce: str | None = None,
        waterfall_id: str | None = None,
        requests_count: int = 0,
        total_bytes: float = 0,
        total_time_ms: int = 0,
    ) -> "AndroidDeviceInstagramAppData":

        if device_id is not None and not is_valid_uuid(device_id):
            raise ValueError(f"Невалидная строка uuidv4")
        if family_device_id is not None and not is_valid_uuid(family_device_id):
            raise ValueError(f"Невалидная строка uuidv4")

        device_id = device_id or str(uuid.uuid4())
        android_id = android_id or generate_android_id_from_guid(device_id)
        family_device_id = family_device_id or str(uuid.uuid4())
        google_ad_id = google_ad_id or str(uuid.uuid4())

        return cls(
            android_id=android_id,
            device_id=device_id,
            family_device_id=family_device_id,
            pigeon_session_id=pigeon_session_id or f"UFS-{uuid.uuid4()}-0",
            google_ad_id=google_ad_id,
            authorization_data=authorization_data or {},
            user_id=user_id,
            mid=mid,
            csrf_token=csrf_token,
            shbid=shbid,
            shbts=shbts,
            rur=rur,
            www_claim=www_claim,
            public_key=public_key,
            public_key_id=public_key_id,
            session_flush_nonce=session_flush_nonce,
            waterfall_id=waterfall_id,
            requests_count=requests_count,
            total_bytes=total_bytes,
            total_time_ms=total_time_ms,
        )

    def set_waterfall_id(self, waterfall_id) -> None:
        self.waterfall_id = waterfall_id

    def set_authorization_data(self, authorization_data: dict[str, str]):
        self.authorization_data = authorization_data
        self.user_id = authorization_data.get("ds_user_id")

    @property
    def authorization(self) -> str | None:
        """
        Возвращает Authorization Header в формате 'Bearer IGT:2:eaW9u.....aWQiOiI0NzM5='
        """

        if self.authorization_data:
            b64part = base64.b64encode(orjson.dumps(self.authorization_data)).decode()
            return f"Bearer IGT:2:{b64part}"
        return None

    @property
    def cookies(self) -> dict:
        cookies = {}

        if self.mid:
            cookies["mid"] = self.mid
        if self.csrf_token:
            cookies["csrftoken"] = self.csrf_token
        if self.rur:
            cookies["rur"] = self.rur
        if self.shbid:
            cookies["shbid"] = self.shbid
        if self.shbts:
            cookies["shbts"] = self.shbts
        if self.authorization_data.get("sessionid"):
            cookies["sessionid"] = self.authorization_data.get("sessionid")
        if self.authorization_data.get("ds_user_id"):
            cookies["ds_user_id"] = self.authorization_data.get("ds_user_id")

        return cookies

    @property
    def cookies_string(self) -> str:
        return (
            ";".join([f"{k}={v}" for k, v in self.cookies.items()])
            if self.cookies
            else ""
        )
