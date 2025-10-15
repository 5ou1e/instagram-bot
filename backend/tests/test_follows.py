
import asyncio
import random
from pathlib import Path

from src.application.common.converters.account.converter import (
    convert_account_entity_to_string, convert_account_string_to_entity)
from src.application.common.converters.account.iam_mob import \
    extract_locale_from_ig_android_user_agent, extract_ig_app_version_from_ig_android_user_agent
from src.application.common.converters.android_device_hardware import \
    android_device_hardware_from_user_agent_string

from src.application.common.types import AccountStringFormat
from src.domain.shared.interfaces.instagram.mobile_client import \
    sync_android_device_instagram_app_data_from_client_local_data, \
    mobile_client_local_data_from_android_device_app_data, \
    mobile_client_device_info_from_android_device
from src.domain.shared.interfaces.instagram.exceptions import UserIdNotFound
from src.domain.shared.interfaces.instagram.mobile_client import \
    MobileInstagramClientNetworkConfig
from src.domain.aggregates.account_worker.entities.account_worker_log.android_device import AndroidDevice, \
    AndroidDeviceInstagramAppData

from src.infrastructure.account_logger import PostgresAccountWorkerLoggerFactory
from src.infrastructure.instagram.mobile_client.builder import \
    MobileInstagramClientBuilderImpl
from src.api.settings.logging import setup_logging

# Глобальная блокировка для записи в файл
file_lock = asyncio.Lock()

WITH_RELOGIN = False
DATA_DIR = Path(r"C:\Python\Мои проекты\insta-bot\data")


with open(DATA_DIR / "айдишки для тестов.txt", "r") as file:
    lines = file.readlines()
    USERS = [str(line.strip()) for line in lines]

USERS = USERS[0:45]


async def do_follows(account, count_follow):
    logger = PostgresAccountWorkerLoggerFactory(queue=asyncio.Queue()).create(
        account_id=account.username
    )

    ua = "Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)"
    instagram_app_version = extract_ig_app_version_from_ig_android_user_agent(
        ua
    )
    locale = extract_locale_from_ig_android_user_agent(ua) or "en_US"
    if not account.android_device:
        account.android_device = AndroidDevice(
            hardware=android_device_hardware_from_user_agent_string(
                ua
            ),
            locale=locale,
            instagram_app_version=instagram_app_version,
            instagram_app_data=AndroidDeviceInstagramAppData.create(),
        )

    # account.proxy = None
    # account.android_device_hardware.profile.timezone = "Europe/Moscow"

    print(f"Аккаунт: {account}")
    print(f"Device: {account.android_device}")
    print(f"Session: {account.android_device.instagram_app_data}")
    print(f"Proxy: {account.proxy}")

    local_data = mobile_client_local_data_from_android_device_app_data(account.android_device.instagram_app_data)
    device_info = mobile_client_device_info_from_android_device(
        account.android_device)

    client = MobileInstagramClientBuilderImpl.new(
    ).with_device_info(
        device_info
    ).with_local_data(
        local_data
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

    error = None

    try:
        if WITH_RELOGIN:
            await client.auth.login(account.username, account.password)

            await client.test_auth.send_requests()

            # await client.direct.direct_v2_get_precence()
            # await client.direct.direct_v2_get_pending_requests_preview()
            # await client.direct.direct_v2_inbox()
            #
            # await client.launcher.mobile_config()
            # await client.launcher.rmd()
            # await client.notifications.get_notification_settings()
            # await client.direct.direct_v2_get_presence_active_now()
            # await client.user.get_limited_interactions_reminder()
            #
            # await client.launcher.banyan_banyan()
            #
            # await client.feed.get_reels_tray()
            # await client.feed.get_feed_timeline_b_api()
            # await client.notifications.badge()
            # await client.news.news_inbox()
            # await client.media.blocked()
            # await client.live.get_good_time_for_live()
            # await client.user.get_user_info_by_id(client._state.local_data.user_id)
            #
            # await client.feed.get_feed_timeline_i_api()

            print(f"Авторизовался в инстаграм!")
            await asyncio.sleep(3)

        for val, user_id in enumerate(USERS):
            try:
                await client.user.follow_user(user_id)
            except UserIdNotFound as e:
                print(e)
                continue
            print(f"({val + 1}/{len(USERS)}) Успешно подписался на пользователя: {user_id} ")
            count_follow += 1
            await asyncio.sleep(random.randint(10, 20))
    except Exception as e:
        error = e
    finally:
        sync_android_device_instagram_app_data_from_client_local_data(account.android_device,
                                                                      local_data)
        await client.close()

    return count_follow, error


async def process_account(account, count_follow):
    comment = "Успешно"
    try:
        count_follow, error = await do_follows(account, count_follow)

        if error:
            comment = f"Завершилось ошибкой: {str(error)[:200]}"
            raise error

    except Exception as e:
        comment = f"Завершилось ошибкой: {str(e)[:200]}"
        print(e)
        raise e
    finally:
        acc_string = convert_account_entity_to_string(account)
        acc_string += f"|{count_follow}|{comment}"

        async with file_lock:
            with open(DATA_DIR / "done_mf.txt", "a+") as file:
                file.write(acc_string)
                file.write("\n")


async def main():
    accounts = []
    with open(DATA_DIR / "workers.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            account = convert_account_string_to_entity(str(line.strip()), format=AccountStringFormat.IAM_MOB)
            if len(line.split("|")) >= 7:
                count_follow = int(line.split("|")[6])
            else:
                count_follow = 0
            accounts.append((account, count_follow))

    results = await asyncio.gather(
        *[process_account(account[0], account[1]) for account in accounts],
        return_exceptions=True
    )

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Аккаунт '{accounts[i][0].username}' ошибка: {result}")
        else:
            print(f"Аккаунт '{accounts[i][0].username}' успех: {result}")

if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
