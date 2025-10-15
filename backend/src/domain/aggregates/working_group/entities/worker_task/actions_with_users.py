from dataclasses import dataclass, field

from src.domain.aggregates.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)


@dataclass(kw_only=True)
class AccountWorkerPerformActionsWithUsersTaskConfig:
    pass


@dataclass(kw_only=True)
class AccountWorkerPerformActionsWithUsersTask(AccountWorkerTask):
    type: AccountWorkerTaskType = AccountWorkerTaskType.ACTIONS_WITH_USERS
    config: AccountWorkerPerformActionsWithUsersTaskConfig = field(
        default_factory=AccountWorkerPerformActionsWithUsersTaskConfig
    )
