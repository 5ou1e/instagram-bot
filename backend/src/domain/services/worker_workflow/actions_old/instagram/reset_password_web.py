from dataclasses import dataclass

from src.domain.aggregates.account.entities.account import Account
from src.domain.aggregates.working_group.exceptions import AccountDoesNotHaveEmailError
from src.domain.services.email_service import EmailService

from src.domain.shared.utils import current_datetime

@dataclass
class ResetPasswordByEmailActionContext(AccountActionContext):
    email_service: EmailService


class ResetPasswordByEmailActionHandler:
    def __init__(self, ctx: ResetPasswordByEmailActionContext):
        self._ctx = ctx

    async def __call__(self, account: Account, new_password: str) -> None:
        if not account.email:
            raise AccountDoesNotHaveEmailError()
        if not account.email.username:
            raise AccountDoesNotHaveEmailError()

        client = self._ctx.instagram_client

        try:
            await self._ctx.logger.info(
                f"Восстанавливаю пароль через почту: %s", account.email.username
            )
            async with self._ctx.uow:
                account.last_action_time = current_datetime()
                account.status = "Восстанавливаю пароль через почту"
                await self._ctx.account_repository.update(account)

            reset_time = current_datetime()
            async with client:
                await client.request_reset_password(
                    account.username,
                    account.email.username,
                )
                await self._ctx.logger.info("Запросил сброс пароля")

                reset_link = await self._ctx.email_service.wait_for_reset_link(
                    account.email.username,
                    account.email.password,
                    from_datetime=reset_time,
                )
                await self._ctx.logger.info(
                    f"Получил ссылку для сброса пароля: {reset_link}"
                )

                try:
                    await client.change_password_by_link(new_password, reset_link)
                except ChallengeRequired as e:
                    if e.type == ChallengeType.AUTH_PLATFORM_CODE_ENTRY:
                        await self._ctx.logger.info(
                            f"Требуется код подтверждения: {e.challenge_path}"
                        )
                        code = (
                            await self._ctx.email_service.wait_for_auth_challenge_code(
                                account.email.username,
                                account.email.password,
                                from_datetime=reset_time,
                            )
                        )
                        await client.send_verification_code_for_auth_platform_challenge(
                            code,
                            e.challenge_path,
                        )

                await self._ctx.logger.info(
                    "Пароль успешно изменен, новый пароль: %s!",
                    new_password,
                )
                async with self._ctx.uow:
                    account.mark_password_as_reset(new_password)
                    await self._ctx.account_repository.update(account)

        except Exception as e:
            await self._ctx.logger.warning(
                "Не удалось восстановить пароль: %s",
                e,
            )
            async with self._ctx.uow:
                account.mark_password_reset_failed()
                await self._ctx.account_repository.update(account)
            raise
