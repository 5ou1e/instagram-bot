from datetime import datetime

from src.domain.aggregates.imap.entities import IMAP


class EmailClient:
    async def get_reset_password_link(
        self,
        username: str,
        password: str,
        from_email: str,
        imap: IMAP,
        cutoff: datetime,
    ) -> str | None: ...

    async def get_auth_platform_code(
        self,
        username: str,
        password: str,
        from_email: str,
        imap: IMAP,
        cutoff: datetime,
    ) -> str | None: ...
