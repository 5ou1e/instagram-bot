from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class Email:
    username: str
    password: str
