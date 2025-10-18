from dataclasses import dataclass

from src.domain.shared.exceptions import DomainError


@dataclass(kw_only=True, slots=True)
class AccountDoesNotHaveUserId(DomainError):

    @property
    def title(self) -> str:
        return f"У аккаунта отсутствует user_id"
