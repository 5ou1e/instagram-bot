from dataclasses import dataclass
from uuid import UUID


@dataclass(kw_only=True, slots=True)
class IMAP:
    id: UUID
    domain: str
    host: str
    port: int
