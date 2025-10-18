from src.domain.aggregates.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.services.worker_workflow.actions_new.action_flows.utils import \
    build_instagram_client_for_worker
from src.domain.shared.interfaces.instagram.mobile_client.converters import (
    sync_android_device_instagram_app_data_from_client_local_data,
)
from src.domain.shared.interfaces.logger import AccountWorkerLogger


class ActionConfig:
    use_proxy: bool = True


class FollowUserActionExecutor:

    def __init__(
        self,
        worker_logger: AccountWorkerLogger,
    ):
        self._worker_logger = worker_logger

    async def execute(
        self,
        worker: AccountWorker,
        follow_user_id: str,
    ):
        async with build_instagram_client_for_worker(
            worker,
            worker_logger=self._worker_logger,
        ) as instagram_client:
            try:
                await instagram_client.user.follow(follow_user_id)
            finally:
                sync_android_device_instagram_app_data_from_client_local_data(
                    worker.android_device, instagram_client
                )
