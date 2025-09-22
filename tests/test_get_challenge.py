import asyncio
import json
import logging
from copy import deepcopy

from pydantic import BaseModel

from src.application.common.converters.account.iam_mob import \
    convert_account_string_to_entity_iam_mob
from src.application.common.converters.android_device_hardware import \
    android_device_hardware_from_user_agent_string
from src.domain.shared.interfaces.instagram.mobile_client import \
    MobileInstagramClientNetworkConfig
from src.domain.shared.entities.account import AccountIgAppSessionData
from src.domain.shared.entities.android_device import (AndroidDeviceProfile)
from src.domain.android_device.entities import AndroidDevice
from src.domain.shared.exceptions23 import NetworkError
from src.infrastructure.account_logger import PostgresAccountWorkerLoggerFactory
from src.infrastructure.instagram.bloks_utils.utils import find_action
from src.infrastructure.instagram.mobile_client.builder import \
    MobileInstagramClientBuilderImpl
from src.settings.logging import setup_logging
from tests.bloks_tools import BloksResponseParser
from tests.bloks_tools import GetArgResolver


async def main():
    string = 'denver.celestial:NgTIkAHs|Instagram 359.2.0.64.89 Android (28/9; 240dpi; 1080x2113; samsung; sm-a520f; a5y17lte; samsungexynos7; en_US; 671551286)|android-7072495495d1ed08;a78284e9-09e6-43c5-b894-5fa1470475fd;b3c2083f-7663-408b-a71c-0f46182b450c;f042261a-9dd6-41d5-a844-0bc25f805bea|shbid="6379\05460342462632\0541727671313:01f7e233032cef2250d5e947bec752a5739fd951f499c389e3cc4b2dc270cbe4baf6e0f6";shbts="1696135313\05460342462632\0541727671313:01f7663635ffc9154b76c082bfa543e52f0358c37e88443ab0fcbf2fd444e421c38e0f1b";rur="RVA\05460342462632\0541727711724:01f7fc16570f8cb6f117eeb04feaf839562b088f50a45463204daca51d8201d008da0ca0";mid=ZLk2QwABAAHg1OQycadGkcrYfkKc;ig_did=BC930338-5E99-4195-BC53-54B7DAC43D5A;ig_cb=deleted;csrftoken=F7aF3S5Tz6qh5LMf4tSYrrAfXSxCq5S6;ds_user_id=60342462632;sessionid=60342462632%3AFZTFJRtzm363sL%3A13%3AAYdWwoWDfJJvuaXlmE9ZG28GjoyklY3IMhOBMqP1oQ;X-IG-WWW-Claim=hmac.AR08sZ6m0JoBsneWzHnA12VbazlOHFx-D6l6wQahg7gJojgf;|pr.oxylabs.io:7777:customer-ozan_zone10-sesstime-30-sessid-z0sSVxLO:38KZPLp0|oxwppswv@maillsk.com:mpwnypza5737|0'

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

    session_data = deepcopy(account.ig_app_session_data)

    class ChallengeRequiredData(BaseModel):
        url: str
        api_path: str
        hide_webview_header: bool
        lock: bool
        logout: bool
        native_flow: bool
        flow_render_type: bool
        challenge_context: str

    with open(
            r"C:\Python\Мои проекты\insta-bot\tools\resolve_challenge\response_with_challenge.json",
            "r",
            encoding="utf-8") as file:
        response = json.loads(file.read())

    parser = BloksResponseParser(response)

    action = parser.parse_complete_action()
    resolver = GetArgResolver()
    action = resolver.resolve_getarg_references(action)
    print(action)

    needed_action = find_action(action, "bk.action.caa.PresentCheckpointsFlow")

    print(needed_action)

    error_data = json.loads(needed_action[1])["error"]["error_data"]
    print(error_data)

    converted = ChallengeRequiredData(**error_data)
    print(converted)

    try:
        res = await client.auth.get_challenge_required_info(challenge_data=converted)
        print(res)
    except NetworkError as e:
        account.ig_app_session_data = session_data
        raise


if __name__ == "__main__":
    setup_logging(level=logging.DEBUG)
    asyncio.run(main())
