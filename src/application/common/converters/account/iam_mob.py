import base64
import re
from urllib.parse import unquote

import orjson
from uuid6 import uuid7

from src.application.common.converters.android_device_hardware import (
    android_device_hardware_from_user_agent_string,
)
from src.application.common.converters.proxy import convert_proxy_line_to_entity
from src.application.common.exceptions import (
    IncorrectAccountStringError,
    IncorrectAndroidUserAgentString,
    IncorrectProxyStringFormatError,
)
from src.application.common.generators import generate_uuid_v4_string
from src.application.common.validators import (
    is_valid_android_id,
    is_valid_csrftoken,
    is_valid_locale_code,
    is_valid_mid,
    is_valid_uuid4_string,
)
from src.domain.account.entities.account import Account, AccountActionStatistics
from src.domain.account.vallue_objects import Email
from src.domain.android_device.entities import (
    AndroidDevice,
    AndroidDeviceInstagramAppData,
)
from src.domain.shared.interfaces.instagram.version import InstagramAppVersion
from src.domain.shared.utils import (
    generate_android_id_from_guid,
    random_timezone_from_locale_code,
)
from src.infrastructure.instagram.mobile_client import VersionInfoRegistry


def convert_account_string_to_entity_iam_mob(line: str) -> Account:
    """Парсит формат IAM_MOB"""

    parts = line.strip().split("|")

    ig_auth = parts[0]
    if ":" not in ig_auth:
        raise IncorrectAccountStringError(string=line)

    username, password = ig_auth.split(":", 1)

    user_agent_string = parts[1] if len(parts) >= 2 else None
    tech_data_string = parts[2] if len(parts) >= 3 else None
    cookies_string = parts[3] if len(parts) >= 4 else None

    android_device = None
    if user_agent_string or tech_data_string or cookies_string:
        android_device = extract_android_device(
            user_agent_string, tech_data_string, cookies_string
        )

    proxy_string = parts[4] if len(parts) >= 5 else None

    proxy = None
    if proxy_string:
        try:
            proxy = convert_proxy_line_to_entity(proxy_string)
        except IncorrectProxyStringFormatError as e:
            pass

    email_data = parts[5] if len(parts) >= 6 else None
    email = None
    if email_data and ":" in email_data:
        email_username, email_password = email_data.split(":", 1)
        email = Email(
            username=email_username,
            password=email_password,
        )

    try:
        follow_actions_count = int(parts[6])
    except:
        follow_actions_count = 0

    user_id = (
        int(android_device.instagram_app_data.user_id)
        if android_device and android_device.instagram_app_data.user_id
        else None
    )

    return Account(
        id=uuid7(),
        username=username,
        password=password,
        email=email,
        user_id=user_id,
        android_device=android_device,
        proxy=proxy,
        action_statistics=AccountActionStatistics(
            follows=follow_actions_count,
        ),
    )


def extract_android_device(
    user_agent_string: str,
    tech_data_string: str,
    cookies_string: str,
) -> AndroidDevice | None:
    """Извлекает AndroidDevice из user agent и tech_data"""

    # Ищем мобильный user agent
    mobile_ua = None

    if user_agent_string and "Instagram" in user_agent_string:
        ua_parts = user_agent_string.split("Instagram")

        if len(ua_parts) >= 2:
            mobile_ua = "Instagram" + ua_parts[1]

    hardware = None
    if mobile_ua:
        try:
            hardware = android_device_hardware_from_user_agent_string(mobile_ua)
        except IncorrectAndroidUserAgentString:
            pass

    locale = extract_locale_from_ig_android_user_agent(user_agent_string) or "en_US"

    instagram_app_data = extract_instagram_app_data(tech_data_string, cookies_string)

    instagram_app_version = extract_ig_app_version_from_ig_android_user_agent(
        user_agent_string
    )

    timezone = random_timezone_from_locale_code(locale)

    if hardware:
        device_os_version = hardware.os_version
        device_os_api_level = hardware.os_api_level
    else:
        device_os_version = "15"
        device_os_api_level = "35"

    return AndroidDevice(
        id=uuid7(),
        hardware=hardware,
        locale=locale,
        timezone=timezone,
        os_version=device_os_version,
        os_api_level=device_os_api_level,
        instagram_app_data=instagram_app_data,
        instagram_app_version=instagram_app_version,
    )


def extract_instagram_app_data(tech_data_string: str, cookies_string: str):
    parts = tech_data_string.split(";")
    if len(parts) >= 4:
        phone_id = (
            parts[1] if is_valid_uuid4_string(parts[1]) else generate_uuid_v4_string()
        )
        device_id = (
            parts[2] if is_valid_uuid4_string(parts[2]) else generate_uuid_v4_string()
        )
        android_id = (
            parts[0]
            if is_valid_android_id(parts[0])
            else generate_android_id_from_guid(device_id)
        )
        adid = (
            parts[3] if is_valid_uuid4_string(parts[3]) else generate_uuid_v4_string()
        )
    else:
        phone_id = generate_uuid_v4_string()
        device_id = generate_uuid_v4_string()
        android_id = generate_android_id_from_guid(device_id)
        adid = generate_uuid_v4_string()

    cookie_pattern = r"([^=;]+)=([^;]*)"
    cookies = {}

    for match in re.finditer(cookie_pattern, cookies_string):
        key = match.group(1).strip().lower()
        value = unquote(match.group(2).strip('"'))
        if value:  # Пропускаем пустые значения
            cookies[key] = value

    authorization_header = cookies.get("authorization", "")
    authorization_data = {}
    if authorization_header:
        authorization_data = extract_data_from_authorization(authorization_header)

    csrf_token = (
        cookies.get("csrftoken", "")
        if is_valid_csrftoken(cookies.get("csrftoken", ""))
        else None
    )

    mid = cookies.get("mid") or cookies.get("x-mid")

    mid = mid if (mid and is_valid_mid(mid)) else None

    return AndroidDeviceInstagramAppData.create(
        android_id=android_id,
        device_id=device_id,
        family_device_id=phone_id,
        google_ad_id=adid,
        mid=mid,
        csrf_token=csrf_token,
        rur=cookies.get("rur"),
        shbid=cookies.get("shbid"),
        shbts=cookies.get("shbts"),
        authorization_data=authorization_data if authorization_data else None,
        user_id=authorization_data.get("user_id") or cookies.get("ds_user_id"),
    )


def extract_locale_from_ig_android_user_agent(string: str, **kwargs) -> str | None:
    """Парсит локаль из юзер-агента Android"""

    try:
        android_part = string.split("Android (")[1].rstrip(")")
        parts = [p.strip() for p in android_part.split(";")]
        locale = parts[7]

        return locale if is_valid_locale_code(locale) else None
    except (IndexError, ValueError) as e:
        return None


def extract_ig_app_version_from_ig_android_user_agent(
    user_agent: str,
) -> InstagramAppVersion | None:
    pattern = r"Instagram (\d+\.\d+\.\d+\.\d+\.\d+)"
    match = re.search(pattern, user_agent)

    if match:
        try:
            return InstagramAppVersion(match.group(1))
        except ValueError:
            pass

    return None


def extract_data_from_authorization(authorization: str) -> dict:
    """Parse authorization header"""

    b64part = authorization.rsplit(":", 1)[-1]
    if not b64part:
        return {}
    return orjson.loads(base64.b64decode(b64part))


def convert_account_entity_to_string_iam_mob(account: Account):
    pattern = "{username}:{password}|{user_agent}|{tech_data}|{cookies}|{proxy}|{email_username}:{email_password}"

    user_agent = ""
    cookies = ""
    tech_data = ""
    device = account.android_device

    if device:
        app_data = account.android_device.instagram_app_data
        user_agent = instagram_user_agent_from_android_device(device)
        if app_data:
            cookies = account.android_device.instagram_app_data.cookies_string
            aurhotization_header = app_data.authorization
            if aurhotization_header:
                cookies += f";Authorization={aurhotization_header}"

            tech_data = (
                "{android_id};{family_device_id};{device_id};{google_ad_id};".format(
                    android_id=app_data.android_id or "",
                    device_id=app_data.device_id or "",
                    family_device_id=app_data.family_device_id or "",
                    google_ad_id=app_data.google_ad_id or "",
                )
            )

    return pattern.format(
        username=account.username or "",
        password=account.password or "",
        user_agent=user_agent,
        tech_data=tech_data,
        cookies=cookies,
        proxy=account.proxy.url if account.proxy else "",
        email_username=account.email.username if account.email else "",
        email_password=account.email.password if account.email else "",
    )


def instagram_user_agent_from_android_device(device: AndroidDevice) -> str:
    version_info = VersionInfoRegistry.get(
        device.instagram_app_version or InstagramAppVersion.V374
    )
    return (
        f"Instagram {version_info.app_version} "
        f"Android ({device.os_api_level}/{device.os_version}; "
        f"{device.hardware.dpi}dpi; {device.hardware.resolution}; "
        f"{device.hardware.manufacturer}/{device.hardware.brand}; {device.hardware.model}; "
        f"{device.hardware.device}; {device.hardware.cpu}; {device.locale}; "
        f"{version_info.version_code})"
    )
