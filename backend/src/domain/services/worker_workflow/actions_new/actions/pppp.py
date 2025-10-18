from src.domain.services.worker_workflow.actions_new.actions.authorize_account import (
    AuthorizeAccountActionExecutor,
)
from src.domain.services.worker_workflow.actions_new.actions.common.change_proxy import (
    ChangeProxyActionExecutor,
)
from src.domain.services.worker_workflow.actions_new.actions.follow_user import (
    FollowUserActionExecutor,
)


class ActionExecutorFactory:

    def __init__(self):
        pass

    def create_change_proxy_action_executor(self) -> ChangeProxyActionExecutor:
        return ChangeProxyActionExecutor()

    def create_authorize_account_action_executor(
        self,
    ) -> AuthorizeAccountActionExecutor:
        return AuthorizeAccountActionExecutor()

    def create_folow_user_action_executor(self) -> FollowUserActionExecutor:
        return FollowUserActionExecutor()
