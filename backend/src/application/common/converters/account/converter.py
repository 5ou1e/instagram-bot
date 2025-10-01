from src.application.common.converters.account.default import (
    convert_account_entity_to_string_default,
    convert_account_string_to_entity_default,
)
from src.application.common.converters.account.iam_mob import (
    convert_account_entity_to_string_iam_mob,
    convert_account_string_to_entity_iam_mob,
)
from src.application.common.types import AccountStringFormat
from src.domain.account.entities.account import Account


def convert_account_string_to_entity(
    line: str,
    format: AccountStringFormat = AccountStringFormat.IAM_MOB,
) -> Account:
    """Конвертирует строку аккаунта в сущность Account"""

    if format == AccountStringFormat.DEFAULT:
        return convert_account_string_to_entity_default(line)
    elif format == AccountStringFormat.IAM_MOB:
        return convert_account_string_to_entity_iam_mob(line)
    else:
        raise ValueError(f"Unknown format: {format}")


def convert_account_entity_to_string(
    entity: Account,
    format_: AccountStringFormat = AccountStringFormat.IAM_MOB,
):
    """Конвертирует сущность Account в строкy"""

    if format_ == AccountStringFormat.DEFAULT:
        return convert_account_entity_to_string_default(entity)
    elif format_ == AccountStringFormat.IAM_MOB:
        return convert_account_entity_to_string_iam_mob(entity)

    else:
        raise ValueError(f"Unknown format: {format_}")
