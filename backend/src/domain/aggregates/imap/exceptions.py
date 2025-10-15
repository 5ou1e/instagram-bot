from dataclasses import dataclass

from src.domain.shared.interfaces.email_client.exceptions import EmailClientError


@dataclass(kw_only=True, slots=True)
class IMAPNotFoundForEmailDomain(EmailClientError):
    domain: str

    @property
    def title(self) -> str:
        return f"Не найден IMAP для домена: {self.domain}"
