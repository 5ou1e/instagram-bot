import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from src.domain.aggregates.account.entities.account import Account
from src.domain.shared.interfaces.instagram.exceptions import ChallengeRequired
from src.domain.services.worker_workflow.actions_old.instagram.base import Flow, FlowConfig, FlowContext


@dataclass
class UnauthorizedFlowConfig(FlowConfig):
    """Конфигурация для неавторзованного flow"""


@dataclass(kw_only=True)
class UnauthorizedFlowContext(FlowContext):
    pass


TContext = TypeVar("TContext", bound=UnauthorizedFlowContext)

TConfig = TypeVar("TConfig", bound=UnauthorizedFlowConfig)


class UnauthorizedFlow(
    Flow[TContext, TConfig],
    Generic[TContext, TConfig],
    ABC,
):
    """Базовый класс для неавторизованных actions_old"""

    def __init__(
        self,
        ctx: TContext,
        config: TConfig,
    ):
        super().__init__(ctx, config)

    @abstractmethod
    async def _execute_action(self, account: Account, *args, **kwargs) -> Any:
        """Выполняет конкретное действие"""

    async def _execute(self, account: Account, *args, **kwargs) -> Any:

        last_error = None
        start_time = asyncio.get_event_loop().time()

        for attempt in range(1, self._config.max_attempts + 1):
            # Проверяем общий таймаут
            try:
                return await self._execute_action(account, *args, **kwargs)

            except ChallengeRequired as challenge:
                raise
                # if not self._config.handle_challenges:
                #     raise
                #
                # await self._logger.info(f"Чекпоинт: {challenge.type}")
                # try:
                #     await self._challenge_resolver.execute(challenge)
                #     return await self._execute_action(account, *args, **kwargs)
                # except Exception as challenge_error:
                #     await self._logger.error(
                #         f"Не удалось пройти challenge: {challenge_error}"
                #     )
                #     last_error = challenge_error

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
