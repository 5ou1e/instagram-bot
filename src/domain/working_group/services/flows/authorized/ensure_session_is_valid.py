from dataclasses import dataclass
from typing import Any

from src.domain.account.flows.authorized.base import (
    AuthorizedFlow,
    AuthorizedFlowConfig,
    AuthorizedFlowContext,
)
from src.domain.shared.utils import current_datetime
from src.domain.working_group.entities.worker.entity import AccountWorker
from src.domain.working_group.exceptions import AccountDoesNotHaveSessionIdError


@dataclass(kw_only=True)
class EnsureSessionIsValidFlowContext(AuthorizedFlowContext):
    pass


@dataclass(kw_only=True)
class EnsureSessionIsValidFlowConfig(AuthorizedFlowConfig):
    pass


class EnsureSessionIsValidFlow(
    AuthorizedFlow[EnsureSessionIsValidFlowContext, EnsureSessionIsValidFlowConfig]
):
    """
    Флоу для валидации существующей сессии.
    """

    async def execute(
        self,
        worker: AccountWorker,
    ) -> None:
        return await self._execute(worker)

    async def _execute_action(
        self,
        worker: AccountWorker,
        *args,
        **kwargs,
    ) -> Any:
        async with self._build_instagram_client(worker) as client:
            try:
                await self._ctx.logger.info(f"Проверяю валидность сессии")

                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    worker.status = "Проверяю валидность сессии"
                    await self._ctx.account_repository.update(worker)

                sessionid = worker.cookies.get("sessionid")
                if not sessionid:
                    raise AccountDoesNotHaveSessionIdError()

                await self._ig_action_wrapper.execute(
                    lambda: client.authorize_by_sessionid(sessionid),
                    worker,
                    client,
                )

                await self._ctx.logger.info("Сессия валидна")

                # Сохраняем куки после успешной авторизации
                async with self._ctx.uow:
                    worker.set_cookies(client.get_cookies())
                    await self._ctx.account_repository.update(worker)

            except Exception as e:
                await self._ctx.logger.warning(
                    "Не удалось проверить валидность сессии: %s", e
                )

                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    await self._ctx.account_repository.update(worker)

                raise
