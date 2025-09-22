from src.application.common.converters.account.converter import (
    convert_account_entity_to_string,
)
from src.domain.account.entities.account import Account
from src.infrastructure.files.file import File


class AccountResetPassResultFileWriter:

    def __init__(self, file: File):
        self._file = file

    async def write(self, account: Account) -> None:
        line = convert_account_entity_to_string(account)
        await self._file.write(line)


class AccountResetPassSuccessResultFileWriter(AccountResetPassResultFileWriter):
    """Записывает аккаунты успешно восстановившие пароль в файл"""

    ...


class AccountResetPassFailedResultFileWriter(AccountResetPassResultFileWriter):
    """Записывает аккаунты которые не смогли восстановить пароль в файл"""

    ...
