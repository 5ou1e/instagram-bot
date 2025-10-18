import asyncio
from uuid import UUID

from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.aggregates.working_group.entities.working_group.entity import (
    WorkingGroup,
)
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.services.email_service import EmailService
from src.domain.services.worker_workflow.actions_old.instagram.unauthorized.reset_password_by_email import (
    ResetPasswordByEmailFlow,
    ResetPasswordByEmailFlowConfig,
    ResetPasswordByEmailFlowContext,
)
from src.domain.services.worker_workflow.working_group_workflow.tasks.base import (
    AccountWorkerTaskExecutor,
)
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.utils import generate_random_password


class AccountWorkerResetPasswordByEmailTaskExecutor(AccountWorkerTaskExecutor):

    def __init__(
        self,
        task_id: UUID,
        uow: Uow,
        working_group_repository: WorkingGroupRepository,
        account_repository: AccountRepository,
        email_service: EmailService,
        logger: Logger,
    ):
        self._task_id = task_id
        self._uow = uow
        self._working_group_repository = working_group_repository
        self._account_repository = account_repository
        self._email_service = email_service
        self._worker_logger = logger

    async def execute(self, account_id: UUID, stop_event: asyncio.Event):
        """Запускаем лоигику задачи"""

        async with self._uow:
            account = await self._account_repository.get_by_id(account_id)
            task: WorkingGroup = await self._working_group_repository.get_by_id(
                subtask.working_group_id
            )

        task_config: WorkingGroupConfig = task.config
        subtask_config = subtask.config

        try:
            new_password = generate_random_password()
            await self._worker_logger.info(f"Сгенерирован новый пароль: {new_password}")

            reset_password_flow = self._create_action_flow(task_config)
            await reset_password_flow.execute(account, new_password)

            await self._success_writer.write(account)
        except Exception as e:
            await self._failed_writer.write(account)
            raise

    def _create_action_flow(
        self, task_config: WorkingGroupConfig
    ) -> ResetPasswordByEmailFlow:
        return ResetPasswordByEmailFlow(
            ctx=ResetPasswordByEmailFlowContext(
                uow=self._uow,
                account_repository=self._account_repository,
                email_service=self._email_service,
                logger=self._worker_logger,
            ),
            config=ResetPasswordByEmailFlowConfig(
                instagram_network_config=task_config.instagram_network_config,
            ),
        )
