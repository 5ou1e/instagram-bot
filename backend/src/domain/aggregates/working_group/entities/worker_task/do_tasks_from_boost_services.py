from dataclasses import dataclass, field

from src.domain.aggregates.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)


@dataclass(kw_only=True)
class AccountWorkerDoTasksFromBoostServicesTaskConfig:
    pass


@dataclass(kw_only=True)
class AccountWorkerDoTasksFromBoostServicesTask(AccountWorkerTask):
    type: AccountWorkerTaskType = AccountWorkerTaskType.DO_TASKS_FROM_BOOST_SERVICES
    config: AccountWorkerDoTasksFromBoostServicesTaskConfig = field(
        default_factory=AccountWorkerDoTasksFromBoostServicesTaskConfig
    )
