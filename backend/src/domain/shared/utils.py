import hashlib
import random
import secrets
import string
import uuid
from datetime import datetime, timezone

from babel import Locale
from pytz import country_timezones


def is_valid_uuid(uuid_string, version=None):
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return version is None or uuid_obj.version == version
    except ValueError:
        return False


def current_datetime() -> datetime:
    return datetime.now(timezone.utc)


def random_timezone_from_locale_code(locale_code: str) -> str:
    # 1. Получаем страну из locale
    loc = Locale.parse(locale_code)
    country_code = loc.territory  # 'RU', 'US', и т.д.

    # 2. Получаем список таймзон этой страны
    timezones = country_timezones.get(country_code)

    return random.choice(timezones)


def generate_random_password(length: int = 8):
    """
    Генерирует случайный пароль.
    """
    if length < 6:
        raise ValueError("Длина пароля должна быть минимум 6 символов")

    # Наборы символов
    letters = string.ascii_letters  # A-Za-z
    digits = string.digits  # 0-9
    specials = string.punctuation  # Специальные символы

    # Гарантируем наличие каждого типа символов
    password_chars = [
        secrets.choice(letters),
        secrets.choice(digits),
    ]
    # Остальные символы — из всех категорий
    all_chars = letters + digits
    password_chars += [secrets.choice(all_chars) for _ in range(length - 3)]

    # Перемешиваем результат
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def generate_android_id_from_guid(guid: uuid.UUID) -> str:
    """
    Генерирует Android Device ID из UUID

    Parameters
    ----------
    guid : uuid.UUID
        Входной UUID

    Returns
    -------
    str
        Android-совместимый device ID
    """

    md5_hash = hashlib.md5(str(guid).encode()).hexdigest()
    return f"android-{md5_hash[:16]}"


def generate_waterfall_id():
    """Генерирует waterfall_id в формате UUID4"""
    return str(uuid.uuid4())
