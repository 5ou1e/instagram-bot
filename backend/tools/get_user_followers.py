import asyncio

from src.application.common.converters.account.iam_mob import \
    convert_account_string_to_entity_iam_mob
from src.application.common.converters.android_device_hardware import \
    android_device_hardware_from_user_agent_string
from src.domain.shared.interfaces.instagram.mobile_client import \
    MobileInstagramClientNetworkConfig
from src.domain.shared.entities.account import AccountIgAppSessionData
from src.domain.shared.entities.android_device import (AndroidDeviceProfile)
from src.domain.aggregates.account_worker.entities.android_device import AndroidDevice
from src.infrastructure.account_logger import PostgresAccountWorkerLoggerFactory
from src.infrastructure.instagram.mobile_client.builder import \
    MobileInstagramClientBuilderImpl
from src.settings.logging import setup_logging


async def main():

    string = 'anjas_dssk97:IG9IMTJha8aG|Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung/samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)|android-dcf4b72e82a08913;c7789434-9daf-43c3-85b3-ab2c134b3832;91136961-c663-4681-b9a3-5cdd59829731;6bc55540-aea4-452e-b1a4-4ac1ab134857;|Authorization=Bearer IGT:2:eyJkc191c2VyX2lkIjoiNjAzNDAzNDg0NzIiLCJzZXNzaW9uaWQiOiI2MDM0MDM0ODQ3MiUzQVdKb1g4Nnk2aW5EZjhJJTNBMjMlM0FBWWQxeThjUU9BM3RBTVp2d1pRUmEzQ25UU01yZ0hWa1ZEdktrQ2ZCWGcifQ==;|http://customer-ozan_zone10-sesstime-30-sessid-noIVXnhY:38KZPLp0@pr.oxylabs.io:7777|qgvzbbdm@maillsk.com:almbimff8757|18|'

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
    max_id = 0
    all_users = []
    for i in range(5):
        users = await client.user.get_user_followers_by_user_id(user_id, max_id=max_id)
        all_users.extend(users)
        max_id += 25

    unique_pks = set()
    for user in all_users:
        unique_pks.add(user["pk"])

    for pk in unique_pks:
        print(pk)

if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
