from src.application.common.types import AccountStringFormat
from src.application.features.working_group.worker.converters.iam_mob import (
    extract_worker_create_dto_from_string_iam_mob,
)
from src.application.features.working_group.worker.dto import AccountWorkerCreateDTO


def extract_worker_create_dto_from_string(
    string: str,
    format_: AccountStringFormat = AccountStringFormat.IAM_MOB,
) -> AccountWorkerCreateDTO:
    """Конвертирует строку аккаунта в сущность Account"""

    if format_ == AccountStringFormat.IAM_MOB:
        return extract_worker_create_dto_from_string_iam_mob(string=string)
    else:
        raise ValueError(f"Unknown format: {format_}")
