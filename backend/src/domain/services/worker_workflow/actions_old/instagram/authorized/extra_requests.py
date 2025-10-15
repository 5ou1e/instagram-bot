from dataclasses import dataclass
from typing import Any

from src.domain.aggregates.account_worker.entities.account_worker_log.account_worker.entity import (
    AccountWorker,
)
from src.domain.services.worker_workflow.action_flows.utils import \
    sync_android_device_instagram_app_data_from_client_local_data
from src.domain.services.worker_workflow.actions_old.instagram.authorized.base import (
    AuthorizedFlow,
    AuthorizedFlowConfig,
    AuthorizedFlowContext,
)
from src.domain.shared.interfaces.instagram.exceptions import FeedbackRequiredError
from src.domain.shared.utils import current_datetime


@dataclass(kw_only=True)
class SendExtraRequestsFlowContext(AuthorizedFlowContext):
    pass


@dataclass(kw_only=True)
class SendExtraRequestsFlowConfig(AuthorizedFlowConfig):
    pass


class SendExtraRequestsFlow(AuthorizedFlow[AuthorizedFlowContext, SendExtraRequestsFlowConfig]):
    """
    Флоу для подписки на пользователя.
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
                await self._ctx.logger.info(f"Отправляю доп.запросы")
                await self._ig_action_wrapper.execute(
                    lambda: client.test_auth.send_requests(),
                    worker,
                    client,
                )
            except Exception as e:
                await self._ctx.logger.warning("Не удалось отправить доп.запросы: %s", e)
                raise
