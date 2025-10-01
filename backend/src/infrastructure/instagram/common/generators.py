import random
import secrets
import time
import uuid
from datetime import datetime, timezone

import pytz

from src.infrastructure.instagram.common.utils import dumps_orjson


def current_timestamp() -> int:
    return int(datetime.now(timezone.utc).timestamp())


def current_timestamp_ms() -> int:
    return int(time.time() * 1000)


def timestamp_with_ms_str(decimals=3) -> str:
    return f"{time.time():.{decimals}f}"


def pigeon_rawclienttime() -> str:
    """1753084231.273"""
    return timestamp_with_ms_str()


def timezone_offset() -> int:
    # # Для Москвы (UTC+3)
    # timezone_offset = "10800"
    # # Для UTC-5
    # timezone_offset = "-18000"
    pass


def generate_nonce():
    """Генерирует криптографически стойкий nonce (64 символа base64)"""
    return secrets.token_urlsafe(48)  # 48 байт -> 64 base64 символа


def generate_uuid_v4_hex() -> str:
    return uuid.uuid4().hex


def generate_uuid_v4_string():
    return str(uuid.uuid4())


def utc_timezone_offset(timezone: str) -> int:
    """Возвращает разницу часовых поясов в секундах"""
    now = datetime.now(pytz.timezone(timezone))
    return int(now.utcoffset().total_seconds())


def device_languages_from_device_locale(locale: str) -> str:
    system_locale = locale.replace("_", "-")

    # 80% шанс использовать system_locale, 20% — en-US
    if random.random() < 0.8:
        keyboard_locale = system_locale
    else:
        keyboard_locale = "en-US"

    return dumps_orjson(
        {
            "system_languages": system_locale,
            "keyboard_language": keyboard_locale,
        }
    )


def generate_network_properties():
    dhcp, local = fake_192_dhcp_and_local()
    ipv6 = f"fe80::cafe:babe:{random.randint(0x1000, 0xffff):x}"

    return f"dhcpServerAddr={dhcp};" f"LocalAddrs=/{ipv6},/{local},;"


def fake_192_dhcp_and_local():
    third = random.randint(0, 255)
    dhcp = f"192.168.{third}.1"
    local = f"192.168.{third}.{random.randint(2, 254)}"
    return dhcp, local
