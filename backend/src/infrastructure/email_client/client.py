from datetime import datetime

from imap_tools import AND, MailBox
from imap_tools import errors as imap_errors

from src.domain.imap.entities import IMAP
from src.domain.shared.interfaces.email_client.client import EmailClient
from src.domain.shared.interfaces.email_client.exceptions import (
    EmailAuthenticationFailed,
)
from src.infrastructure.email_client.utils import (
    parse_auth_platform_code_from_message,
    parse_url_from_html_message,
)


class DefaultEmailClient(EmailClient):
    async def get_reset_password_link(
        self,
        username: str,
        password: str,
        from_email: str,
        imap: IMAP,
        cutoff: datetime,
    ) -> str | None:

        try:
            with MailBox(imap.host).login(username, password, "INBOX") as mailbox:
                for msg in mailbox.fetch(AND(from_=from_email), reverse=True, limit=10):
                    if msg.date >= cutoff:
                        url = await parse_url_from_html_message(msg.html)
                        if url:
                            return url
        except imap_errors.MailboxLoginError as e:
            raise EmailAuthenticationFailed(message=str(e))

        return None

    async def get_auth_platform_code(
        self,
        username: str,
        password: str,
        from_email: str,
        imap: IMAP,
        cutoff: datetime,
    ) -> str | None:
        try:
            with MailBox(imap.host).login(username, password, "INBOX") as mailbox:
                for msg in mailbox.fetch(AND(from_=from_email), reverse=True, limit=10):
                    if msg.date >= cutoff:
                        code = await parse_auth_platform_code_from_message(msg.html)
                        if code:
                            return code
        except imap_errors.MailboxLoginError as e:
            raise EmailAuthenticationFailed(message=str(e))

        return None
