from sqlalchemy import Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class ProxyModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "proxy"

    protocol: Mapped[str] = mapped_column(String(20))
    host: Mapped[str] = mapped_column(Text)
    port: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)

    usage: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )

    workers = relationship("AccountWorkerModel", back_populates="proxy")

    __table_args__ = (
        UniqueConstraint(
            "protocol", "host", "port", "username", "password", name="uq_proxy"
        ),
    )
