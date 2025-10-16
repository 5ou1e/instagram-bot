from uuid import UUID

from pydantic import BaseModel


class SetAccountsCommentRequest(BaseModel):
    account_ids: list[UUID]
    comment: str | None
