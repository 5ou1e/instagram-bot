import base64
import re
from typing import Optional
from urllib.parse import unquote

import orjson

from src.application.common.converters.android_device_hardware import (
    android_device_hardware_from_user_agent_string,
)
from src.application.common.exceptions import (
    IncorrectAccountStringError,
    IncorrectAndroidUserAgentString,
)
from src.application.common.generators import generate_uuid_v4_string
from src.application.common.validators import (
    is_valid_android_id,
    is_valid_csrftoken,
    is_valid_locale_code,
    is_valid_mid,
    is_valid_uuid4_string,
)
from src.application.features.working_group.worker.dto import (
    AccountWorkerCreateAccountDTO,
    AccountWorkerCreateAndroidDeviceDTO,
    AccountWorkerCreateAndroidDeviceHardwareDTO,
    AccountWorkerCreateDTO,
    AccountWorkerCreateProxyDTO,
)
from src.domain.android_device_hardware.entities.android_device import AndroidDevice, \
    AndroidDeviceInstagramAppData
from src.domain.shared.interfaces.instagram.version import InstagramAppVersion
from src.domain.shared.utils import (
    generate_android_id_from_guid,
    random_timezone_from_locale_code,
)
from src.domain.account_worker.entities.account_worker.entity import AccountWorker
from src.infrastructure.instagram.mobile_client import VersionInfoRegistry


def extract_worker_create_dto_from_string_iam_mob(
    string: str,
) -> AccountWorkerCreateDTO:
    parts = string.strip().split("|")

    # --- account ---
    ig_auth = parts[0]
    if ":" not in ig_auth:
        raise IncorrectAccountStringError(string=string)
    username, password = ig_auth.split(":", 1)

    email_username, email_password = None, None
    if len(parts) >= 6 and ":" in parts[5]:
        email_username, email_password = parts[5].split(":", 1)

    try:
        follow_actions_count = int(parts[6])
    except Exception:
        follow_actions_count = 0

    account_dto = AccountWorkerCreateAccountDTO(
        username=username,
        password=password,
        email_username=email_username,
        email_password=email_password,
        user_id=None,  # можно достать позже из app_data
        follow_actions_count=follow_actions_count,
    )

    # --- proxy ---
    proxy_dto = None
    if len(parts) >= 5 and parts[4]:
        proxy_dto = AccountWorkerCreateProxyDTO(raw_proxy_string=parts[4])

    # --- device ---
    android_device_dto = None
    if len(parts) >= 2:
        user_agent_string = parts[1]
        tech_data_string = parts[2] if len(parts) >= 3 else None
        cookies_string = parts[3] if len(parts) >= 4 else None
        android_device_dto = extract_android_device_dto(
            user_agent_string, tech_data_string, cookies_string
        )

    return AccountWorkerCreateDTO(
        account=account_dto,
        proxy=proxy_dto,
        android_device=android_device_dto,
    )


def extract_android_device_dto(
    user_agent_string: str,
    tech_data_string: str,
    cookies_string: str,
) -> Optional[AccountWorkerCreateAndroidDeviceDTO]:
    mobile_ua = None
    if user_agent_string and "Instagram" in user_agent_string:
        ua_parts = user_agent_string.split("Instagram")
        if len(ua_parts) >= 2:
            mobile_ua = "Instagram" + ua_parts[1]

    hardware_dto = None
    if mobile_ua:
        try:
            hw = android_device_hardware_from_user_agent_string(mobile_ua)
            hardware_dto = AccountWorkerCreateAndroidDeviceHardwareDTO(
                manufacturer=hw.manufacturer,
                brand=hw.brand,
                model=hw.model,
                device=hw.device,
                cpu=hw.cpu,
                dpi=hw.dpi,
                resolution=hw.resolution,
                os_version=hw.os_version,
                os_api_level=hw.os_api_level,
            )
        except IncorrectAndroidUserAgentString:
            pass

    locale = extract_locale_from_ig_android_user_agent(user_agent_string) or "en_US"
    instagram_app_data = extract_instagram_app_data(tech_data_string, cookies_string)
    instagram_app_version = extract_ig_app_version_from_ig_android_user_agent(
        user_agent_string
    )
    timezone = random_timezone_from_locale_code(locale)

    return AccountWorkerCreateAndroidDeviceDTO(
        hardware=hardware_dto,
        os_version=hardware_dto.os_version if hardware_dto else "15",
        os_api_level=hardware_dto.os_api_level if hardware_dto else "35",
        locale=locale,
        timezone=timezone,
        connection_type="WIFI",
        instagram_app_version=instagram_app_version or InstagramAppVersion.V374,
        instagram_app_data=instagram_app_data,
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


def convert_account_worker_entity_to_string_iam_mob(worker: AccountWorker):
    pattern = "{username}:{password}|{user_agent}|{tech_data}|{cookies}|{proxy}|{email_username}:{email_password}"

    user_agent = ""
    cookies = ""
    tech_data = ""
    device = worker.android_device

    if device:
        app_data = worker.android_device.instagram_app_data
        user_agent = instagram_user_agent_from_android_device(device)
        if app_data:
            cookies = worker.android_device.instagram_app_data.cookies_string
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
        username=worker.username or "",
        password=worker.password or "",
        user_agent=user_agent,
        tech_data=tech_data,
        cookies=cookies,
        proxy=worker.proxy.url if worker.proxy else "",
        email_username=worker.email.username if worker.email else "",
        email_password=worker.email.password if worker.email else "",
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
