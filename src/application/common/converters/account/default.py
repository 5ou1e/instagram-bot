import json

from uuid6 import uuid7

from src.application.common.exceptions import IncorrectAccountStringError
from src.domain.account.entities.account import Account


def convert_account_string_to_entity_default(string: str):
    # TODO наверное лучше это сделать через Pydantic
    try:
        account_dict = json.loads(string)
        return Account(
            id=uuid7(),
            username=account_dict["username"],
            password=account_dict["password"],
        )
    except Exception:
        raise IncorrectAccountStringError


def convert_account_entity_to_string_default(entity: Account):
    fields = ["username", "password", "email", "android_device", "proxy"]
    account_dict = entity.to_dict()

    for field in account_dict.copy().keys():
        if field not in fields:
            account_dict.pop(field)

    return json.dumps(account_dict)
