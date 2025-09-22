import re
from urllib.parse import parse_qs, urlparse

from src.infrastructure.instagram.web_client.types import ParamsFromResetPassUrl


def parse_password_reset_recovery_success_client(json_data) -> bool:
    tree = json_data["layout"]["bloks_payload"]["tree"]
    action = tree["bk.components.internal.Action"]
    handler = action["handler"]

    match = re.search(r'"(password_reset_recovery_success_client)"', handler)
    if match:
        return True
    return False


def extract_payload_data_from_reset_password_url(url: str) -> ParamsFromResetPassUrl:
    parsed_url = urlparse(url)

    query_params = parse_qs(parsed_url.query)
    token = query_params.get("token", [None])[0]
    uidb36 = query_params.get("uidb36", [None])[0]
    source = query_params.get("s", [None])[0]
    is_caa = True if query_params.get("is_caa", [None])[0] else False
    afv = query_params.get("afv", [None])[0]

    data = ParamsFromResetPassUrl(
        token=token,
        uidb36=uidb36,
        source=source,
        is_caa=is_caa,
        afv=afv,
    )

    return data


def extract_masked_email(text):
    # Здесь * внутри [], поэтому не нужно экранировать
    match = re.search(r"\b[\w*]+@[\w*]+\.\w+\b", text)
    return match.group(0) if match else None
