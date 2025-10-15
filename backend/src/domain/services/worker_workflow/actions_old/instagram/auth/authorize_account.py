import asyncio
from dataclasses import dataclass
from typing import Any

from src.domain.aggregates.account_worker.entities.account_worker.entity import (
    AccountWorker,
)
from src.domain.services.worker_workflow.actions_old.instagram.base import (
    Flow,
    FlowConfig,
    FlowContext,
)
from src.domain.services.worker_workflow.actions_old.instagram.unauthorized.reset_password_by_email import (
    ResetPasswordByEmailFlow,
)
from src.domain.shared.interfaces.instagram.exceptions import (
    BadPassword,
    ChallengeRequired,
)
from src.domain.shared.interfaces.instagram.mobile_client.converters import (
    sync_android_device_instagram_app_data_from_client_local_data,
)
from src.domain.shared.utils import current_datetime, generate_random_password


@dataclass
class AuthorizationFlowConfig(FlowConfig):
    """Конфигурация поведения при авторизации"""

    # Поведение при неверном пароле
    on_bad_password_change_password_by_email: bool = False


@dataclass(kw_only=True)
class AuthorizationFlowContext(FlowContext):
    pass


class AuthorizationFlow(
    Flow[AuthorizationFlowContext, AuthorizationFlowConfig],
):
    """
    Авторизация
    """

    def __init__(
        self,
        ctx: AuthorizationFlowContext,
        config: AuthorizationFlowConfig,
        reset_password_flow: ResetPasswordByEmailFlow | None = None,
    ):
        super().__init__(ctx, config)
        self._reset_password_flow = reset_password_flow
        # self._challenge_resolver = ChallengeResolver()

    async def _execute_action(
        self,
        worker: AccountWorker,
        *args,
        **kwargs,
    ) -> Any:
        async with self._build_instagram_client(worker) as client:
            try:
                await self._ctx.logger.info(f"Прохожу авторизацию")

                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    worker.status = "Прохожу авторизацию"
                    await self._ctx.account_worker_repository.update(worker)

                    account = await self._ctx.account_repository.get_by_id(
                        worker.account_id
                    )

                auth_result = await self._ig_action_wrapper.execute(
                    lambda: client.auth.login(account.username, account.password),
                    worker,
                    client,
                )
                await self._ig_action_wrapper.execute(
                    lambda: client.test_auth.send_requests(),
                    worker,
                    client,
                )

                await self._ctx.logger.info("Успешно авторизовался")

                # Сохраняем данные после успешной авторизации
                async with self._ctx.uow:
                    sync_android_device_instagram_app_data_from_client_local_data(
                        worker.android_device, client
                    )
                    account.set_user_id(
                        int(worker.android_device.instagram_app_data.user_id)
                    )
                    account.action_statistics.authorizations += 1
                    worker.last_action_time = current_datetime()

                    await self._ctx.account_worker_repository.update(worker)
                    await self._ctx.account_repository.update(account)

                return auth_result

            except Exception as e:
                await self._ctx.logger.warning("Не удалось пройти авторизацию: %s", e)
                raise

    async def execute(
        self,
        worker: AccountWorker,
    ):
        last_error = None

        for attempt in range(1, self._config.max_attempts + 1):
            try:
                return await self._execute_action(
                    worker,
                )

            except ChallengeRequired as challenge:
                raise
                # if not self._config.handle_challenges:
                #     raise
                #
                # await self._logger.info(f"Чекпоинт: {challenge.type}")
                # try:
                #     await self._logger.info(f"Прохождение чекпоинтов не реализовано")
                #     raise challenge
                #     # await self._challenge_resolver.execute(challenge)
                # except Exception as challenge_error:
                #     last_error = challenge_error
                #     break
                # else:
                #     return await self._execute_action(account)

            except BadPassword as e:
                if (
                    self._config.on_bad_password_change_password_by_email
                    and self._reset_password_flow
                ):
                    new_password = generate_random_password()
                    try:
                        await self._reset_password_flow.execute(worker, new_password)
                        return await self._execute_action(worker)
                    except Exception as reset_error:
                        last_error = reset_error
                else:
                    if (
                        not self._reset_password_flow
                        and self._config.on_bad_password_change_password_by_email
                    ):
                        await self._logger.error(
                            "Восстановление пароля включено, но reset_password_flow не предоставлен"
                        )
                    raise

            except Exception as e:
                if not any(
                    isinstance(e, exc_type)
                    for exc_type in self._config.retryable_exceptions
                ):
                    raise
                last_error = e

            if attempt < self._config.max_attempts:
                await asyncio.sleep(self._config.retry_delay)

        raise last_error
