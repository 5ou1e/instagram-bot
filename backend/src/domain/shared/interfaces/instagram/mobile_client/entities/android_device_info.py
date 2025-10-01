from dataclasses import dataclass
from typing import Literal


@dataclass
class MobileClientAndroidDeviceInfo:

    name: str  # "Xiaomi Redm Note 8"
    manufacturer: str  # "Xiaomi"
    brand: str  # "xiaomi"
    model: str  # "Redm Note 8"
    device: str  # "ginkgo"
    cpu: str  # "qcom"
    dpi: str  # "440"
    resolution: str  # "1080x2130"
    os_version: str  # "10"
    os_api_level: str  # "29"

    locale: str = "en_US"
    timezone: str = "Europe/Madrid"
    connection_type: Literal["WIFI", "MOBILE(LTE)"] = "WIFI"
