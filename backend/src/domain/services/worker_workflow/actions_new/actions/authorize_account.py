from src.domain.aggregates.account.repository import AccountRepository
from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker

from src.domain.aggregates.account_worker.repositories.account_worker import (
    AccountWorkerRepository,
)
from src.domain.services.worker_workflow.actions_new.action_flows.utils import \
    build_instagram_client_for_worker, sync_android_device_instagram_app_data_from_client_local_data
from src.domain.shared.interfaces.logger import AccountWorkerLogger
from src.domain.shared.interfaces.uow import Uow
from src.domain.shared.utils import current_datetime


class AuthorizeAccountActionExecutor:

    def __init__(
        self,
        uow: Uow,
        account_worker_repository: AccountWorkerRepository,
        account_repository: AccountRepository,
        worker_logger: AccountWorkerLogger,
    ):
        self.uow = uow
        self.account_worker_repository = account_worker_repository
        self.account_repository = account_repository
        self._worker_logger = worker_logger

    async def execute(self, worker: AccountWorker):
        # TODO тут подумать, как не ходить за аккаунтом каждый раз , если обработка ошибок прокси лежит не здесь.
        #  мб просто хранить снапшот аккаунта в сущности Worker-a
        #  в целом  не критично

        async with build_instagram_client_for_worker(
            worker,
            worker_logger=self._worker_logger,
        ) as instagram_client:
            async with self.uow:
                account = await self.account_repository.get_by_id(worker.account_id)
            try:
                auth_result = await instagram_client.auth.login()
            finally:
                sync_android_device_instagram_app_data_from_client_local_data(
                    worker.android_device, instagram_client
                )

                # Сохраняем данные после успешной авторизации
                async with self.uow:
                    sync_android_device_instagram_app_data_from_client_local_data(
                        worker.android_device, instagram_client
                    )
                    account.set_user_id(
                        int(worker.android_device.instagram_app_data.user_id)
                    )
                    account.action_statistics.authorizations += 1
                    worker.last_action_time = current_datetime()

                    await self.account_worker_repository.update(worker)
                    await self.account_repository.update(account)

                return auth_result
