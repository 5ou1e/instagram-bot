import asyncio
from uuid import UUID

from src.domain.account.repositories.account import AccountRepository
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.services.email_service import EmailService
from src.domain.shared.utils import generate_random_password
from src.domain.working_group.entities.config.working_group_config import (
    WorkingGroupConfig,
)
from src.domain.working_group.entities.working_group.entity import WorkingGroup
from src.domain.working_group.repositories.account_worker_task import (
    AccountWorkerTaskRepository,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.domain.working_group.services.flows.unauthorized.reset_password_by_email_flow import (
    ResetPasswordByEmailFlow,
    ResetPasswordByEmailFlowConfig,
    ResetPasswordByEmailFlowContext,
)
from src.domain.working_group.services.task_executors.base import (
    AccountWorkerTaskExecutor,
)
from src.infrastructure.files.file_writer import (
    AccountResetPassFailedResultFileWriter,
    AccountResetPassSuccessResultFileWriter,
)


class AccountWorkerResetPasswordByEmailTaskExecutor(AccountWorkerTaskExecutor):

    def __init__(
        self,
        subtask_id: UUID,
        uow: Uow,
        account_worker_task_repository: AccountWorkerTaskRepository,
        working_group_repository: WorkingGroupRepository,
        account_repository: AccountRepository,
        email_service: EmailService,
        logger: Logger,
        success_writer: AccountResetPassSuccessResultFileWriter,
        failed_writer: AccountResetPassFailedResultFileWriter,
    ):
        self._subtask_id = subtask_id
        self._uow = uow
        self._account_worker_task_repository = account_worker_task_repository
        self._working_group_repository = working_group_repository
        self._account_repository = account_repository
        self._email_service = email_service
        self._logger = logger
        self._success_writer = success_writer
        self._failed_writer = failed_writer

    async def execute(self, account_id: UUID, stop_event: asyncio.Event):
        """Запускаем лоигику задачи"""

        async with self._uow:
            subtask = await self._account_worker_task_repository.get_by_id(
                self._subtask_id
            )
            account = await self._account_repository.get_by_id(account_id)
            task: WorkingGroup = await self._working_group_repository.get_by_id(
                subtask.working_group_id
            )

        task_config: WorkingGroupConfig = task.config
        subtask_config = subtask.config

        try:
            new_password = generate_random_password()
            await self._logger.info(f"Сгенерирован новый пароль: {new_password}")

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
                logger=self._logger,
            ),
            config=ResetPasswordByEmailFlowConfig(
                instagram_network_config=task_config.instagram_network_config,
            ),
        )
