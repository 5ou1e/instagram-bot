import random
import urllib

import orjson


def build_signed_body(data):
    """Generate signature of POST data for Private API

    Returns
    -------
    str
        e.g. "signed_body=SIGNATURE.test"
    """
    return "signed_body=SIGNATURE.{data}".format(data=urllib.parse.quote_plus(data))


def dumps_orjson(data):
    """JSON dumps using orjson, Instagram-compatible compact format"""
    return orjson.dumps(data, option=orjson.OPT_NON_STR_KEYS).decode("utf-8")


def calculate_bandwith_speed(total_bytes=0, total_time_ms=0):

    # Рассчитываем speed с коэффициентом 0.18 ± 30%
    if total_time_ms == 0:
        speed = 531  # константа для первого/кэшированного запроса
    else:
        base_speed = (total_bytes * 8) / total_time_ms
        coefficient = 0.18 * random.uniform(0.7, 1.3)  # ±30% от 0.18
        speed = base_speed * coefficient

    return speed


def instagram_app_user_agent_from_android_device_info(
    device_info: "MobileClientAndroidDeviceInfo",
    version_info: "InstagramAppVersionInfo",
) -> str:
    return (
        f"Instagram {version_info.app_version} "
        f"Android ({device_info.os_api_level}/{device_info.os_version}; "
        f"{device_info.dpi}dpi; {device_info.resolution}; "
        f"{device_info.manufacturer}/{device_info.brand}; {device_info.model}; "
        f"{device_info.device}; {device_info.cpu}; {device_info.locale}; "
        f"{version_info.version_code})"
    )
