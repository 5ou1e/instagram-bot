from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.repositories.models.common import (
    Base,
    TimestampsMixin,
    UUIDIDMixin,
)


class IMAPModel(Base, UUIDIDMixin, TimestampsMixin):
    __tablename__ = "imap"

    domain: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    host: Mapped[str] = mapped_column(Text, nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
