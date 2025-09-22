from src.domain.account.repositories.account import AccountRepository
from src.domain.shared.interfaces.logger import Logger
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.services.email_service import EmailServiceFactory
from src.domain.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)
from src.domain.working_group.repositories.account_worker import AccountWorkerRepository
from src.domain.working_group.repositories.account_worker_task import (
    AccountWorkerTaskRepository,
)
from src.domain.working_group.repositories.working_group import WorkingGroupRepository
from src.domain.working_group.services.providers.proxy_provider import ProxyProvider
from src.domain.working_group.services.task_executors.actions_with_users import (
    AccountWorkerActionsWithUsersTaskExecutor,
)
from src.domain.working_group.services.task_executors.authorize import (
    AccountWorkerAuthorizeAccountTaskExecutor,
)
from src.domain.working_group.services.task_executors.base import (
    AccountWorkerTaskExecutor,
)
from src.domain.working_group.services.task_executors.do_tasks_from_boost_services import (
    AccountWorkerDoTasksFromBoostServicesTaskExecutor,
)
from src.domain.working_group.services.task_executors.reset_password_by_email import (
    AccountWorkerResetPasswordByEmailTaskExecutor,
)
from src.infrastructure.files.file_writer import (
    AccountResetPassFailedResultFileWriter,
    AccountResetPassSuccessResultFileWriter,
)


class AccountWorkerTaskExecutorFactory:
    """Создает AccountWorkerTaskExecutor для переданной задачи"""

    def __init__(
        self,
        uow: Uow,
        account_repository: AccountRepository,
        account_worker_repository: AccountWorkerRepository,
        email_service_factory: EmailServiceFactory,
        account_worker_task_repository: AccountWorkerTaskRepository,
        proxy_provider: ProxyProvider,
        working_group_repository: WorkingGroupRepository,
        account_reset_password_success_writer: AccountResetPassSuccessResultFileWriter,
        account_reset_password_failed_writer: AccountResetPassFailedResultFileWriter,
    ):
        self._uow = uow
        self._proxy_provider = proxy_provider
        self._account_repository = account_repository
        self._account_worker_repository = account_worker_repository
        self._account_worker_task_repository = account_worker_task_repository
        self._working_group_repository = working_group_repository
        self._email_service_factory = email_service_factory
        self._account_reset_password_success_writer = (
            account_reset_password_success_writer
        )
        self._account_reset_password_failed_writer = (
            account_reset_password_failed_writer
        )

    def create(
        self,
        task: AccountWorkerTask,
        account_logger: Logger,
    ) -> AccountWorkerTaskExecutor:
        """Возвращает обработчик задачи аккаунт-воркера"""

        if task.type == AccountWorkerTaskType.AUTHORIZE_ACCOUNT:
            return AccountWorkerAuthorizeAccountTaskExecutor(
                subtask_id=task.id,
                uow=self._uow,
                account_worker_task_repository=self._account_worker_task_repository,
                working_group_repository=self._working_group_repository,
                account_repository=self._account_repository,
                logger=account_logger,
                email_service=self._email_service_factory.create(account_logger),
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
            )
        elif task.type == AccountWorkerTaskType.DO_TASKS_FROM_BOOST_SERVICES:
            return AccountWorkerDoTasksFromBoostServicesTaskExecutor(
                subtask_id=task.id,
                uow=self._uow,
                account_worker_task_repository=self._account_worker_task_repository,
                working_group_repository=self._working_group_repository,
                account_repository=self._account_repository,
                logger=account_logger,
                proxy_provider=self._proxy_provider,
            )
        elif task.type == AccountWorkerTaskType.ACTIONS_WITH_USERS:
            return AccountWorkerActionsWithUsersTaskExecutor(
                subtask_id=task.id,
                uow=self._uow,
                account_worker_task_repository=self._account_worker_task_repository,
                working_group_repository=self._working_group_repository,
                account_repository=self._account_repository,
                logger=account_logger,
                proxy_provider=self._proxy_provider,
            )
        elif task.type == AccountWorkerTaskType.RESET_PASSWORD_BY_EMAIL:
            return AccountWorkerResetPasswordByEmailTaskExecutor(
                subtask_id=task.id,
                uow=self._uow,
                account_worker_task_repository=self._account_worker_task_repository,
                account_repository=self._account_repository,
                working_group_repository=self._working_group_repository,
                email_service=self._email_service_factory.create(account_logger),
                logger=account_logger,
                success_writer=self._account_reset_password_success_writer,
                failed_writer=self._account_reset_password_failed_writer,
            )
        raise ValueError(f"Нет обработчика для задачи {task.type}")
