from src.domain.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.account_worker.services.actions.base import AccountWorkerActionExecutor
from src.domain.account_worker.services.actions.build_instagram_client import \
    _build_instagram_client
from src.domain.shared.interfaces.instagram.mobile_client.converters import \
    sync_android_device_instagram_app_data_from_client_local_data
from src.domain.shared.utils import current_datetime


class AuthorizeAccountActionExecutor(AccountWorkerActionExecutor):
    def __init__(self):
        pass

    async def execute(self, worker: AccountWorker):
        async with _build_instagram_client(worker) as client:
            try:
                await self._ctx.logger.info(f"Прохожу авторизацию")

                async with self._ctx.uow:
                    worker.last_action_time = current_datetime()
                    worker.status = "Прохожу авторизацию"
                    await self._ctx.account_worker_repository.update(worker)

                    account = await self._ctx.account_repository.get_by_id(
                        worker.account_id
                    )

                auth_result = await self._ig_action_wrapper.execute(
                    lambda: client.auth.login(account.username, account.password),
                    worker,
                    client,
                )
                await self._ig_action_wrapper.execute(
                    lambda: client.test_auth.send_requests(),
                    worker,
                    client,
                )

                await self._ctx.logger.info("Успешно авторизовался")

                # Сохраняем данные после успешной авторизации
                async with self._ctx.uow:
                    sync_android_device_instagram_app_data_from_client_local_data(
                        worker.android_device, client
                    )
                    account.set_user_id(
                        int(worker.android_device.instagram_app_data.user_id)
                    )
                    account.action_statistics.authorizations += 1
                    worker.last_action_time = current_datetime()

                    await self._ctx.account_worker_repository.update(worker)
                    await self._ctx.account_repository.update(account)

                return auth_result

            except Exception as e:
                await self._ctx.logger.warning("Не удалось пройти авторизацию: %s", e)
                raise
