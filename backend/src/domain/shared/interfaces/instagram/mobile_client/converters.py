from src.domain.aggregates.account_worker.entities.account_worker_log.android_device import (
    AndroidDevice,
    AndroidDeviceInstagramAppData,
)
from src.domain.shared.interfaces.instagram.mobile_client.entities.android_device_info import (
    MobileClientAndroidDeviceInfo,
)
from src.domain.shared.interfaces.instagram.mobile_client.entities.local_data import (
    MobileInstagramClientLocalData,
)


def sync_android_device_instagram_app_data_from_client_local_data(
    android_device: AndroidDevice,
    client: "MobileInstagramClient",
) -> None:
    """Синхронизация данных из клиента обратно в доменную модель"""
    local_data = client.get_local_data()
    app_data = android_device.instagram_app_data

    app_data.authorization_data = local_data.authorization_data.copy()
    app_data.user_id = local_data.user_id
    app_data.mid = local_data.mid
    app_data.csrf_token = local_data.csrf_token
    app_data.shbid = local_data.shbid
    app_data.shbts = local_data.shbts
    app_data.rur = local_data.rur
    app_data.www_claim = local_data.www_claim
    app_data.public_key = local_data.public_key
    app_data.public_key_id = local_data.public_key_id
    app_data.session_flush_nonce = local_data.session_flush_nonce

    app_data.waterfall_id = local_data.waterfall_id
    app_data.pigeon_session_id = local_data.pigeon_session_id

    app_data.requests_count = local_data.requests_count
    app_data.total_bytes = local_data.total_bytes
    app_data.total_time_ms = local_data.total_time_ms


def mobile_client_local_data_from_android_device_app_data(
    app_data: AndroidDeviceInstagramAppData,
) -> MobileInstagramClientLocalData:
    # Конвертируем Android-device app_data в local_data

    return MobileInstagramClientLocalData(
        android_id=app_data.android_id,
        device_id=app_data.device_id,
        family_device_id=app_data.family_device_id,
        google_ad_id=app_data.google_ad_id,
        pigeon_session_id=app_data.pigeon_session_id,
        authorization_data=app_data.authorization_data.copy(),
        user_id=app_data.user_id,
        mid=app_data.mid,
        csrf_token=app_data.csrf_token,
        shbid=app_data.shbid,
        shbts=app_data.shbts,
        rur=app_data.rur,
        www_claim=app_data.www_claim,
        public_key=app_data.public_key,
        public_key_id=app_data.public_key_id,
        session_flush_nonce=app_data.session_flush_nonce,
        waterfall_id=app_data.waterfall_id,
        requests_count=app_data.requests_count,
        total_bytes=app_data.total_bytes,
        total_time_ms=app_data.total_time_ms,
    )


def mobile_client_device_info_from_android_device(
    android_device: AndroidDevice,
) -> MobileClientAndroidDeviceInfo:
    if not android_device.hardware:
        raise ValueError(f"Отсутствуют Hardware характеристики у Android устройства")

    return MobileClientAndroidDeviceInfo(
        name=android_device.hardware.name,
        manufacturer=android_device.hardware.manufacturer,
        brand=android_device.hardware.brand,
        model=android_device.hardware.model,
        device=android_device.hardware.device,
        cpu=android_device.hardware.cpu,
        dpi=android_device.hardware.dpi,
        resolution=android_device.hardware.resolution,
        os_version=android_device.os_version,  # Берем из AndroidDevice
        os_api_level=android_device.os_api_level,  # Берем из AndroidDevice
        locale=android_device.locale,
        timezone=android_device.timezone,
        connection_type=android_device.connection_type,
    )
