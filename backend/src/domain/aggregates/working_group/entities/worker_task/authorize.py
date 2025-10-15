from dataclasses import dataclass, field

from src.domain.aggregates.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)


@dataclass(kw_only=True)
class AccountWorkerAuthoirizeAccountTaskConfig:
    pass


@dataclass(kw_only=True)
class AccountWorkerAuthoirizeAccountTask(AccountWorkerTask):
    type: AccountWorkerTaskType = AccountWorkerTaskType.AUTHORIZE_ACCOUNT
    config: AccountWorkerAuthoirizeAccountTaskConfig = field(
        default_factory=AccountWorkerAuthoirizeAccountTaskConfig
    )
