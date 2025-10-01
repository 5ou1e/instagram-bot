import re
import string
import uuid

from babel import Locale


def is_valid_mid(mid: str):
    pattern = r"^[a-zA-Z0-9+/_-]{28}$"
    return bool(re.match(pattern, mid))


def is_valid_csrftoken(csrftoken: str):
    return is_valid_token(csrftoken, 64)


def is_valid_token(token: str, size: int = 64, symbols: bool = False) -> bool:
    """
    Проверяет, что строка соответствует формату сгенерированного токена
    """
    if len(token) != size:
        return False

    if symbols:
        # Буквы, цифры и символы пунктуации
        pattern = f"^[a-zA-Z0-9{re.escape(string.punctuation)}]{{{size}}}$"
    else:
        # Только буквы и цифры
        pattern = f"^[a-zA-Z0-9]{{{size}}}$"

    return bool(re.match(pattern, token))


def is_valid_android_id(android_id: str) -> bool:
    pattern = r"^android-[a-f0-9]{16}$"
    return bool(re.match(pattern, android_id))


def is_valid_uuid4_string(uuid_string):
    try:
        return uuid.UUID(uuid_string).version == 4
    except ValueError:
        return False


def is_valid_locale_code(locale_code: str) -> bool:
    try:
        Locale.parse(locale_code)
        return True
    except Exception as e:
        return False
