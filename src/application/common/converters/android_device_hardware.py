from uuid6 import uuid7

from src.application.common.exceptions import IncorrectAndroidUserAgentString
from src.domain.android_device.entities import AndroidDeviceHardware
from src.domain.shared.utils import current_datetime


def android_device_hardware_from_user_agent_string(
    string: str,
    **kwargs,
) -> AndroidDeviceHardware:
    """Создает AndroidDeviceHardware из User-Agent строки"""

    try:
        android_part = string.split("Android (")[1].rstrip(")")
        parts = [p.strip() for p in android_part.split(";")]

        if len(parts) != 9:
            raise IncorrectAndroidUserAgentString(string=string)

        android_api_level, android_version = parts[0].split("/")
        dpi = parts[1].replace("dpi", "")
        resolution = parts[2]

        # Manufacturer может содержать слеш (manufacturer/brand)
        manufacturer_part = parts[3]
        if "/" in manufacturer_part:
            manufacturer, brand = manufacturer_part.split("/", 1)
        else:
            manufacturer = manufacturer_part
            brand = manufacturer_part.lower()

        model = parts[4]
        device = parts[5]
        cpu = parts[6]

    except (IndexError, ValueError) as e:
        raise IncorrectAndroidUserAgentString(string=string) from e

    name = f"{manufacturer} {model}"

    return AndroidDeviceHardware(
        id=uuid7(),
        name=name,
        os_version=android_version,
        os_api_level=android_api_level,
        dpi=dpi,
        resolution=resolution,
        manufacturer=manufacturer,
        brand=brand,
        model=model,
        device=device,
        cpu=cpu,
        created_at=current_datetime(),
        updated_at=current_datetime(),
    )
