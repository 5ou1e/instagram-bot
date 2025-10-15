from dataclasses import dataclass
from typing import Any

from src.domain.aggregates.account_worker.entities.account_worker_log.account_worker.entity import (
    AccountWorker,
)
from src.domain.services.worker_workflow.actions_old.instagram.authorized.base import (
    AuthorizedFlow,
    AuthorizedFlowConfig,
    AuthorizedFlowContext,
)
from src.domain.shared.interfaces.instagram.exceptions import FeedbackRequiredError


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
            async with self._ctx.uow:
                account = await self._ctx.account_repository.get_by_id(
                    worker.account_id
                )

            try:
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
                    account.action_statistics.follows += 1
                    await self._ctx.account_repository.update(account)

            except FeedbackRequiredError as e:
                await self._ctx.logger.info(f"Действие заблокировано: {e}")
                async with self._ctx.uow:
                    account.action_statistics.follows_blocks += 1
                    await self._ctx.account_repository.update(account)

                raise

            except Exception as e:
                await self._ctx.logger.info(f"Не смог подписаться: {e}")
                raise e

            finally:
                await client.close()

            return
