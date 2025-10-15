from src.domain.aggregates.account_worker.entities.account_worker_log.account_worker.entity import (
    AccountWorker,
)
from src.domain.services.account_worker.action_flows.instagram.authorize_account import (
    AuthorizeAccountFlowExecutor,
)
from src.domain.services.account_worker.actions.common.change_proxy import (
    ChangeProxyActionExecutor,
)
from src.domain.services.account_worker.actions.follow_user import (
    FollowUserActionExecutor,
)
from src.domain.shared.interfaces.instagram.exceptions import UnauthorizedError
from src.domain.shared.interfaces.logger import AccountWorkerLogger


class FollowUserFlowExecutor:

    def __init__(
        self,
        follow_action_executor: FollowUserActionExecutor,
        change_proxy_action_executor: ChangeProxyActionExecutor,
        authorize_account_flow_executor: AuthorizeAccountFlowExecutor,
        worker_logger: AccountWorkerLogger,
    ):
        self.follow_action_executor = follow_action_executor
        self.change_proxy_action_executor = change_proxy_action_executor
        self.authorize_account_flow_executor = authorize_account_flow_executor
        self.worker_logger = worker_logger

    async def execute(
        self,
        worker: AccountWorker,
        follow_user_id: str,
    ):
        while True:
            try:
                await self.follow_action_executor.execute(worker, follow_user_id)
            except UnauthorizedError as e:
                await self.worker_logger.warning(
                    f"Не смог подписаться, Instagram сбросил авторизацию"
                )

                # if reauthorize_on_unauthorized
                await self.authorize_account_action_executor.execute(worker)
                continue
            # except Unauthorized as e:
            #     self.authorize_account_action_executor.execute()
            # except NetworkError as e:
            #     self.change_proxy_action_executor.execute()
