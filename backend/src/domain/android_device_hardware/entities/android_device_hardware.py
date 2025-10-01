import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.domain.shared.utils import (
    current_datetime,
)


@dataclass(kw_only=True, slots=True)
class AndroidDeviceHardware:
    """Модель устройства (hardware характеристики)"""

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

    created_at: datetime = field(default_factory=current_datetime)
    updated_at: datetime = field(default_factory=current_datetime)

    @property
    def unique_key(self) -> tuple:
        return (
            self.manufacturer,
            self.model,
            self.device,
            self.resolution,
        )


