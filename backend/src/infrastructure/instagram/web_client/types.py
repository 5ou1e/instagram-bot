from typing import TypedDict


class ParamsFromResetPassUrl(TypedDict):
    token: str
    uidb36: str
    source: str
    is_caa: bool
    afv: str
