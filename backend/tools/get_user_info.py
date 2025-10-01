import asyncio

from src.application.common.converters.account.iam_mob import \
    convert_account_string_to_entity_iam_mob
from src.application.common.converters.android_device_hardware import \
    android_device_hardware_from_user_agent_string


from src.domain.android_device_hardware.entities.android_device import AndroidDevice


from src.domain.shared.interfaces.instagram.mobile_client.config import \
    MobileInstagramClientNetworkConfig
from src.infrastructure.instagram.mobile_client.builder import \
    MobileInstagramClientBuilderImpl



async def main():
    string = 'anjas_dssk97:IG9IMTJha8aG|Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung/samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)|android-dcf4b72e82a08913;c7789434-9daf-43c3-85b3-ab2c134b3832;91136961-c663-4681-b9a3-5cdd59829731;6bc55540-aea4-452e-b1a4-4ac1ab134857;|Authorization=Bearer IGT:2:eyJkc191c2VyX2lkIjoiNjAzNDg2NDIyMjgiLCJzZXNzaW9uaWQiOiI2MDM0ODY0MjIyOCUzQXRzVlhFQXNKYjdScm05JTNBNCUzQUFZZEUxeVlsZzdXMGFCNlNkWmVPb3BEWUVkRTFHZFg4bi11by1QY1NqZyJ9;IG-U-DS-USER-ID=60348642228;|http://customer-ozan_zone10-sesstime-30-sessid-noIVXnhY:38KZPLp0@pr.oxylabs.io:7777|qgvzbbdm@maillsk.com:almbimff8757|18|'

    account = convert_account_string_to_entity_iam_mob(str(string.strip()))

    logger = PostgresAccountWorkerLoggerFactory(queue=asyncio.Queue()).create(
        account_id=account.username
    )

    if not account.android_device:
        account.android_device = AndroidDevice(
            spec=android_device_hardware_from_user_agent_string(
                "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)"
            ),
            profile=AndroidDeviceProfile.create(
                locale="en_US",
                timezone="Europe/Madrid",
            )
        )

    account.proxy = None

    if not account.ig_app_session_data:
        account.ig_app_session_data = AccountIgAppSessionData()

    client = MobileInstagramClientBuilderImpl.new(
    ).with_device(
        account.android_device
    ).with_local_data(
        account.ig_app_session_data
    ).with_network_config(
        MobileInstagramClientNetworkConfig(
            proxy=account.proxy,
            max_network_wait_time=20,
            max_retries_on_network_errors=0,
            delay_before_retries_on_network_errors=0,
        )
    ).with_logger(
        logger
    ).build()

    print(f"Аккаунт: {account}")
    print(f"Device: {account.android_device}")
    print(f"Session: {account.ig_app_session_data}")
    print(f"Proxy: {account.proxy}")

    # session_data = deepcopy(account.ig_app_session_data)
    # try:
    #     await client.auth.login(account.username, account.password)
    # except NetworkError as e:
    #     account.ig_app_session_data = session_data
    #     raise

    user_id = "56615472420"
    await client.user.get_user_info_by_id(user_id)


# follower_count
if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
