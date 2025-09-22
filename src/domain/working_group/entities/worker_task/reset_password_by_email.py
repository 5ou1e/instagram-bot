from dataclasses import dataclass, field

from src.domain.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)


@dataclass(kw_only=True)
class AccountWorkerResetPasswordByEmailTaskConfig:
    pass


@dataclass(kw_only=True)
class AccountWorkerResetPasswordByEmailTask(AccountWorkerTask):
    type: AccountWorkerTaskType = AccountWorkerTaskType.RESET_PASSWORD_BY_EMAIL
    config: AccountWorkerResetPasswordByEmailTaskConfig = field(
        default_factory=AccountWorkerResetPasswordByEmailTaskConfig
    )
