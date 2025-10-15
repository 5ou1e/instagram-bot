from dataclasses import dataclass
from typing import Any

from src.domain.aggregates.account.entities.account import Account
from src.domain.aggregates.account_worker.entities.account_worker_log.account_worker.entity import (
    AccountWorker,
)
from src.domain.aggregates.working_group.exceptions import AccountDoesNotHaveEmailError
from src.domain.services.email_service import EmailService
from src.domain.services.worker_workflow.actions_old.instagram.unauthorized.base import (
    UnauthorizedFlow,
    UnauthorizedFlowConfig,
    UnauthorizedFlowContext,
)
from src.domain.shared.interfaces.instagram.exceptions import (
    ChallengeRequired,
    ChallengeType,
)
from src.domain.shared.utils import current_datetime


@dataclass(kw_only=True)
class ResetPasswordByEmailFlowContext(UnauthorizedFlowContext):
    email_service: EmailService


@dataclass(kw_only=True)
class ResetPasswordByEmailFlowConfig(UnauthorizedFlowConfig):
    pass


class ResetPasswordByEmailFlow(
    UnauthorizedFlow[ResetPasswordByEmailFlowContext, ResetPasswordByEmailFlowConfig]
):

    async def execute(
        self,
        account: Account,
        new_password: str,
    ) -> None:
        return await self._execute(account, new_password)

    async def _execute_action(
        self,
        worker: AccountWorker,
        *args,
        **kwargs,
    ) -> Any:
        if not worker.email:
            raise AccountDoesNotHaveEmailError()
        if not worker.email.username:
            raise AccountDoesNotHaveEmailError()
        new_password = args[1]
        async with self._build_instagram_client(worker) as client:

            try:
                await self._ctx.logger.info(
                    f"Восстанавливаю пароль через почту: %s", worker.email.username
                )
                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    worker.status = "Восстанавливаю пароль через почту"
                    await self._ctx.account_repository.update(worker)

                reset_time = current_datetime()
                async with client:
                    await self._ig_action_wrapper.execute(
                        lambda: client.request_reset_password(
                            worker.username,
                            worker.email.username,
                        ),
                        worker,
                        client,
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

                        await self._ig_action_wrapper.execute(
                            lambda: client.change_password_by_link(
                                new_password, reset_link
                            ),
                            account,
                            client,
                        )

                    except ChallengeRequired as e:
                        if e.type == ChallengeType.AUTH_PLATFORM_CODE_ENTRY:
                            await self._ctx.logger.info(
                                f"Требуется код подтверждения: {e.challenge_path}"
                            )
                            code = await self._ctx.email_service.wait_for_auth_challenge_code(
                                account.email.username,
                                account.email.password,
                                from_datetime=reset_time,
                            )

                            await self._ig_action_wrapper.execute(
                                lambda: client.send_verification_code_for_auth_platform_challenge(
                                    code,
                                    e.challenge_path,
                                ),
                                account,
                                client,
                            )

                    await self._ctx.logger.info(
                        "Пароль успешно изменен, новый пароль: %s!",
                        new_password,
                    )
                    async with self._ctx.uow:
                        account.set_password(new_password)
                        await self._ctx.account_repository.update(account)

            except Exception as e:
                await self._ctx.logger.warning(
                    "Не удалось восстановить пароль: %s",
                    e,
                )
                async with self._ctx.uow:
                    await self._ctx.account_repository.update(account)
                raise
