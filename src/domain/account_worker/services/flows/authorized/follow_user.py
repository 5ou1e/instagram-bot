from dataclasses import dataclass
from typing import Any

from src.domain.shared.interfaces.instagram.exceptions import FeedbackRequiredError
from src.domain.shared.utils import current_datetime
from src.domain.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.account_worker.services.flows.authorized.base import (
    AuthorizedFlow,
    AuthorizedFlowConfig,
    AuthorizedFlowContext,
)


@dataclass(kw_only=True)
class FollowUserFlowContext(AuthorizedFlowContext):
    pass


@dataclass(kw_only=True)
class FollowUserFlowConfig(AuthorizedFlowConfig):
    pass


class FollowUserFlow(AuthorizedFlow[AuthorizedFlowContext, FollowUserFlowConfig]):
    """
    Флоу для подписки на пользователя.
    """

    async def execute(
        self,
        worker: AccountWorker,
        user_id: str,
    ) -> None:
        return await self._execute(worker, user_id)

    async def _execute_action(
        self,
        worker: AccountWorker,
        *args,
        **kwargs,
    ) -> Any:
        user_id = args[0]
        async with self._build_instagram_client(worker) as client:

            try:
                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    worker.status = f"Подписываюсь на пользователя"
                    await self._ctx.account_repository.update(worker)

                await self._ctx.logger.info(
                    f"Подписываюсь на пользователя {user_id} ..."
                )

                await self._ig_action_wrapper.execute(
                    lambda: client.user.follow_user(str(user_id)),
                    worker,
                    client,
                )
                await self._ctx.logger.info(f"Подписался на пользователя {user_id}")

                async with self._ctx.uow:
                    worker.action_statistics.follows += 1
                    worker.last_action_time = current_datetime()
                    await self._ctx.account_repository.update(worker)
            except FeedbackRequiredError as e:
                await self._ctx.logger.info(f"Действие заблокировано: {e}")
                worker.action_statistics.follows_blocks += 1
                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    await self._ctx.account_repository.update(worker)
                raise
            except Exception as e:
                await self._ctx.logger.info(f"Не смог подписаться: {e}")
                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    await self._ctx.account_repository.update(worker)
                raise e

            finally:
                await client.close()

            return
