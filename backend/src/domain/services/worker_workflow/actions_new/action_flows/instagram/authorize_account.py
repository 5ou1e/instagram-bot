from src.domain.aggregates.account_worker.entities.account_worker.entity import (
    AccountWorker,
)
from src.domain.services.worker_workflow.actions_new.actions.authorize_account import (
    AuthorizeAccountActionExecutor,
)
from src.domain.services.worker_workflow.actions_new.actions.common.change_proxy import (
    ChangeProxyActionExecutor,
)


class AuthorizeAccountFlowExecutor:
    def __init__(self):
        self.authorize_account_action_executor = AuthorizeAccountActionExecutor()
        self.change_proxy_action_executor = ChangeProxyActionExecutor()

    async def execute(self, worker: AccountWorker):
        await self.authorize_account_action_executor.execute(worker)
