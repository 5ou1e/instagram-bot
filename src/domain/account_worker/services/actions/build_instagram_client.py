from src.domain.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.shared.interfaces.instagram.mobile_client.client import MobileInstagramClient
from src.domain.shared.interfaces.instagram.mobile_client.config import \
    MobileInstagramClientNetworkConfig
from src.domain.shared.interfaces.instagram.mobile_client.converters import \
    mobile_client_local_data_from_android_device_app_data, \
    mobile_client_device_info_from_android_device
from src.domain.shared.interfaces.logger import AccountWorkerLogger
from src.infrastructure.instagram import MobileInstagramClientBuilderImpl


def _build_instagram_client(
    worker: AccountWorker,
    worker_logger: AccountWorkerLogger,
) -> MobileInstagramClient:
    local_data = mobile_client_local_data_from_android_device_app_data(
        worker.android_device.instagram_app_data
    )
    device_info = mobile_client_device_info_from_android_device(
        worker.android_device
    )

    return (
        MobileInstagramClientBuilderImpl.new()
        .with_device_info(device_info)
        .with_local_data(local_data)
        .with_network_config(
            MobileInstagramClientNetworkConfig(
                proxy=worker.proxy,
                max_network_wait_time=20,
                max_retries_on_network_errors=0,
                delay_before_retries_on_network_errors=0,
            )
        )
        .with_logger(worker_logger)
        .build()
    )
