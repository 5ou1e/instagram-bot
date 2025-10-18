from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.aggregates.working_group.entities.worker_task.base import (
    AccountWorkerTask,
    AccountWorkerTaskType,
)
from src.domain.aggregates.working_group.repository import WorkingGroupRepository
from src.domain.services.email_service import EmailServiceFactory
from src.domain.services.worker_workflow.providers.proxy_provider import ProxyProvider
from src.domain.services.worker_workflow.working_group_workflow.tasks.authorize import (
    AccountWorkerAuthorizeAccountTaskExecutor,
)
from src.domain.services.worker_workflow.working_group_workflow.tasks.base import (
    AccountWorkerTaskExecutor,
)
from src.domain.services.worker_workflow.working_group_workflow.tasks.do_tasks_from_boost_services import (
    AccountWorkerDoTasksFromBoostServicesTaskExecutor,
)
from src.domain.shared.interfaces.logger import AccountWorkerLogger
from src.domain.shared.interfaces.uow import Uow


class AccountWorkerTaskExecutorFactory:
    """Создает AccountWorkerTaskExecutor для переданной задачи"""

    def __init__(
        self,
        uow: Uow,
        account_repository: AccountRepository,
        account_worker_repository: AccountWorkerRepository,
        email_service_factory: EmailServiceFactory,
        proxy_provider: ProxyProvider,
        working_group_repository: WorkingGroupRepository,
        worker_logger: AccountWorkerLogger,
    ):
        self._uow = uow
        self._proxy_provider = proxy_provider
        self._account_repository = account_repository
        self._account_worker_repository = account_worker_repository
        self._working_group_repository = working_group_repository
        self._email_service_factory = email_service_factory
        self._worker_logger = worker_logger

    def create(
        self,
        task: AccountWorkerTask,
    ) -> AccountWorkerTaskExecutor:
        """Возвращает обработчик задачи аккаунт-воркера"""

        if task.type == AccountWorkerTaskType.AUTHORIZE_ACCOUNT:
            return AccountWorkerAuthorizeAccountTaskExecutor(
                task_id=task.id,
                uow=self._uow,
                working_group_repository=self._working_group_repository,
                account_repository=self._account_repository,
                email_service=self._email_service_factory.create(self._worker_logger),
                proxy_provider=self._proxy_provider,
                account_worker_repository=self._account_worker_repository,
                logger=self._worker_logger,
            )
        elif task.type == AccountWorkerTaskType.DO_TASKS_FROM_BOOST_SERVICES:
            return AccountWorkerDoTasksFromBoostServicesTaskExecutor(
                task_id=task.id,
                uow=self._uow,
                working_group_repository=self._working_group_repository,
                account_repository=self._account_repository,
                account_worker_repository=self._account_worker_repository,
                proxy_provider=self._proxy_provider,
                logger=self._worker_logger,
            )
        # elif task.type == AccountWorkerTaskType.ACTIONS_WITH_USERS:
        #     return AccountWorkerActionsWithUsersTaskExecutor(
        #         task_id=task.id,
        #         uow=self._uow,
        #         working_group_repository=self._working_group_repository,
        #         account_repository=self._account_repository,
        #
        #         proxy_provider=self._proxy_provider,
        #         logger=self._worker_logger,
        #     )
        # elif task.type == AccountWorkerTaskType.RESET_PASSWORD_BY_EMAIL:
        #     return AccountWorkerResetPasswordByEmailTaskExecutor(
        #         task_id=task.id,
        #         uow=self._uow,
        #         account_repository=self._account_repository,
        #         working_group_repository=self._working_group_repository,
        #         email_service=self._email_service_factory.create(self._worker_logger),
        #         success_writer=self._account_reset_password_success_writer,
        #         failed_writer=self._account_reset_password_failed_writer,
        #         logger=self._worker_logger,
        #     )

        raise ValueError(f"Нет обработчика для задачи {task.type}")
