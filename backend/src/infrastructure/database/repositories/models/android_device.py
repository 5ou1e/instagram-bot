import uuid

from sqlalchemy import UUID
from sqlalchemy import Enum as SaEnum
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.shared.interfaces.instagram.version import InstagramAppVersion
from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class AndroidDeviceHardwareModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "android_device_hardware"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    device: Mapped[str] = mapped_column(String(100), nullable=False)
    cpu: Mapped[str] = mapped_column(String(50), nullable=False)
    os_version: Mapped[str] = mapped_column(String(10), nullable=False)
    os_api_level: Mapped[str] = mapped_column(String(10), nullable=False)
    dpi: Mapped[str] = mapped_column(String(20), nullable=False)
    resolution: Mapped[str] = mapped_column(String(20), nullable=False)

    devices = relationship(
        "AndroidDeviceModel", back_populates="hardware", lazy="noload"
    )

    __table_args__ = (
        UniqueConstraint(
            "manufacturer",
            "model",
            "device",
            "resolution",
            name="uq_android_device_hardware",
        ),
    )


class AndroidDeviceModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "android_device"

    os_version: Mapped[str] = mapped_column(String(10), nullable=False)
    os_api_level: Mapped[str] = mapped_column(String(10), nullable=False)

    locale: Mapped[str] = mapped_column(String(10), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)
    connection_type: Mapped[str] = mapped_column(
        String(20), default="WIFI", nullable=False
    )

    instagram_app_version: Mapped[InstagramAppVersion] = mapped_column(
        SaEnum(
            InstagramAppVersion,
            name="instagram_app_version_enum",
        ),
        nullable=True,
    )

    instagram_app_data: Mapped[dict] = mapped_column(JSON, nullable=True)

    hardware_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("android_device_hardware.id", ondelete="RESTRICT"),
        nullable=True,
    )

    hardware = relationship(
        "AndroidDeviceHardwareModel", back_populates="devices", lazy="joined"
    )

    workers = relationship("AccountWorkerModel", back_populates="android_device")
