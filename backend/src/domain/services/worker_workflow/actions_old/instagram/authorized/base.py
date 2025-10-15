import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from src.domain.aggregates.account_worker.entities.account_worker_log.account_worker.entity import (
    AccountWorker,
)
from src.domain.services.worker_workflow.actions_old.instagram.auth.authorize_account import (
    AuthorizationFlow,
)
from src.domain.services.worker_workflow.actions_old.instagram.base import (
    Flow,
    FlowConfig,
    FlowContext,
)
from src.domain.shared.interfaces.instagram.exceptions import (
    ChallengeRequired,
    UnauthorizedError,
)


@dataclass
class AuthorizedFlowConfig(FlowConfig):
    """Конфигурация для выполнения action flow"""


@dataclass(kw_only=True)
class AuthorizedFlowContext(FlowContext):
    pass


TContext = TypeVar("TContext", bound=AuthorizedFlowContext)

TConfig = TypeVar("TConfig", bound=AuthorizedFlowConfig)


class AuthorizedFlow(
    Flow[TContext, TConfig],
    Generic[TContext, TConfig],
    ABC,
):
    """Базовый класс для всех actions_old с авторизацией"""

    def __init__(
        self,
        ctx: TContext,
        config: TConfig,
        authorization_flow: AuthorizationFlow | None,
    ):
        super().__init__(ctx, config)
        self._authorization_flow = authorization_flow

    @abstractmethod
    async def _execute_action(self, worker: AccountWorker, *args, **kwargs) -> Any:
        """Выполняет конкретное действие"""
        ...

    async def _execute(self, worker: AccountWorker, *args, **kwargs) -> Any:
        last_error = None
        start_time = asyncio.get_event_loop().time()

        for attempt in range(1, self._config.max_attempts + 1):

            try:
                return await self._execute_action(worker, *args, **kwargs)

            except UnauthorizedError as e:
                if not self._config.reauthorize_on_unauthorized:
                    raise

                try:
                    await self._authorization_flow.execute(worker)
                    return await self._execute_action(worker, *args, **kwargs)
                except Exception as auth_error:
                    last_error = auth_error

            except ChallengeRequired as challenge:
                raise
                # if not self._config.handle_challenges:
                #     raise
                # try:
                #     await self._challenge_resolver.execute(challenge)
                #     return await self._execute_action(account, *args, **kwargs)
                # except Exception as challenge_error:
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
