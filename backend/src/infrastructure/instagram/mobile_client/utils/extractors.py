import base64
import re
from urllib.parse import parse_qsl, unquote

import orjson


def extract_data_from_authorization(authorization: str) -> dict:
    """Parse authorization header"""

    b64part = authorization.rsplit(":", 1)[-1]
    if not b64part:
        return {}
    return orjson.loads(base64.b64decode(b64part))


def extract_challenge_path(bloks_payload: dict) -> str | None:
    # Пример ответа для подтверждения по коду с почты\телефона
    r"""{
      "layout": {
        "bloks_payload": {
          "data": [

          ],
          "tree": {
            "bk.components.internal.Action": {
              "handler": "(bk.action.navigation.OpenUrlV2, \"\\/challenge\\/action\\/ASgMlbPzwaZ69EPgoraymtHNh7HKZgJpH6UkDploJyfAgKOe77sJPM7iWeVn1RRDdWnmgQc\\/ASRXeVAsa5brhLpLiQyLfV1Jz3Afb_-7bzkuwV7QLTX5v2KWj2_zrKHKj-NNO7igjbUDvDofWEKfSg\\/ffc_pC572kKQPmguFYjVejTS0g4ExydQWH5IxfhRdTB0fIzyb8sEWkqdfiZ5lwqfo0eu\\/?next=%2Faccounts%2Flogin%2F%3FconfirmReset%3D1\", (bk.action.bloks.InflateSync, (bk.action.map.MakeFlat, \"bk.data.navigation.OpenUrlOptions\", (bk.action.map.MakeFlat))))"
            }
          },
          "embedded_payloads": [

          ],
          "error_attribution": {
            "logging_id": "{\"callsite\":\"{\\\"oncall\\\":\\\"instagram_account_protection\\\",\\\"feature\\\":\\\"PasswordResetSubmitActionHandler\\\",\\\"product\\\":\\\"bloks_async_component\\\"}\",\"push_phase\":\"c2\"}",
            "source_map_id": "(distillery_unknown)"
          }
        }
      },
      "status": "ok"
    }"""

    tree = bloks_payload.get("layout", {}).get("bloks_payload", {}).get("tree", {})

    for node in tree.values():
        handler = node.get("handler", "")
        m = re.search(r'OpenUrlV2,\s*"([^"]+)"', handler)
        if not m:
            continue

        # JSON.loads уже убрал все \/, осталось чистое '/challenge/...'
        raw_url = m.group(1)
        url = unquote(raw_url)

        url = url.replace(r"\/", "/")
        if "challenge" in url and "confirmReset=1" in url:
            return url
        if "auth_platform" in url and "apc" in url:
            url = url.replace("auth_platform", "auth_platform/codeentry")
            return url

    return None


def extract_encrypted_ap_context_from_challenge_path(challenge_path: str) -> str:
    # Оставляем только часть после ?
    name = "apc"
    qs = challenge_path.split("?", 1)[-1]
    # разбираем в список (ключ, значение)
    pairs = parse_qsl(qs, keep_blank_values=True)
    for key, val in pairs:
        if key == name:
            return val
    raise ValueError(f"Параметр 'apc' не найден в challenge_path: {challenge_path}")
