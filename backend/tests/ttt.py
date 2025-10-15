import time

from src.domain.aggregates.account_worker import ChangeProxyActionExecutor
from src.domain.aggregates.account_worker.services import AuthorizeAccountActionExecutor


class FollowUserActionFlowExecutor():

    def __init__(self):
        self.change_proxy_action_executor = ChangeProxyActionExecutor()
        self.authorize_account_action_executor = AuthorizeAccountActionExecutor()

    def execute(self):
        pass


actions = []
for i in range(2_000_000):
    actions.append(FollowUserActionFlowExecutor())
time.sleep(100)
actions[0]