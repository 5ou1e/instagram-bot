from src.domain.account_worker.services.actions_old.change_proxy import \
    AccountWorkerChangeProxyActionExecutor
from src.domain.account_worker.services.actions_old.instagram.auth.authorize_account import \
    AuthorizationFlow
from src.domain.account_worker.services.actions_old.instagram.authorized.follow_user import \
    FollowUserFlow


class AccountWorkerActionExecutorFactory:

    def __init__(self):
        pass

    def create_change_proxy_action_executor(self) -> AccountWorkerChangeProxyActionExecutor:
        return AccountWorkerChangeProxyActionExecutor()

    def create_authorize_account_action_executor(self) -> AuthorizationFlow:
        return AuthorizationFlow()

    def create_folow_user_action_executor(self) -> FollowUserFlow:
        return FollowUserFlow()
