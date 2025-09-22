import json
from json import JSONDecodeError

import aiohttp

from src.domain.shared.interfaces.boost_services.exceptions import *
from src.domain.shared.interfaces.boost_services.venro_client import (
    VenroClient,
    VenroTaskData,
)


class VenroClientImpl(VenroClient):

    def __init__(self):
        self.base_url = "https://thepanel.ru/"
        self.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }

    async def get_task_follow(self, api_key, bot_id, service_id) -> VenroTaskData:
        return await self.get_task(api_key, bot_id, service_id)

    async def get_task_like(self, api_key, bot_id, service_id) -> VenroTaskData:
        return await self.get_task(api_key, bot_id, service_id)

    async def get_task_comment(self, api_key, bot_id, service_id) -> VenroTaskData:
        return await self.get_task(api_key, bot_id, service_id)

    async def get_task(self, api_key, bot_id, service_id) -> VenroTaskData:
        # thepanel.ru/api/do/working_group?key=ключ&bot_id=идаккаунта&type=идуслуги
        # Response example
        # {
        # id: "722426977",
        # code: "emirxsm_x34",
        # item_id: "24492053911",
        # author: "24492053911",
        # # type: "following",
        # money: "0.00009"
        # }

        url = f"{self.base_url}api/do/tasks"

        params = {
            "key": api_key,
            "bot_id": bot_id,
            "type": service_id,
        }

        result = await self._send_request(url, params=params)
        try:
            return VenroTaskData.from_dict(result)
        except Exception as e:
            raise VenroBadResponseError(
                f"Некорректный ответ от Venro, {e}, response={result}"
            )

    async def send_task_done(self, api_key, working_group_id, bot_id, bot_username):
        """Отправляем на проверку"""
        # thepanel.ru/api/do/check?key=ключ&id=идзадания&bot_id=идаккаунта&login=логинаккаунта
        url = f"{self.base_url}api/do/check"

        params = {
            "key": api_key,
            "id": working_group_id,
            "bot_id": bot_id,
            "login": bot_username,
        }

        result = await self._send_request(url, params=params)
        if not result.get("response") == "accepted":
            raise VenroTaskNotAccepted(f"VenroClientError, response={result}")
        return result

    async def send_task_cancel(self, api_key, working_group_id):
        """Отмена задания"""
        # https://thepanel.ru/api/do/bad-check?key=ключ&id=идзадания

        url = f"{self.base_url}api/do/bad-check"
        params = {
            "key": api_key,
            "id": working_group_id,
        }
        result = await self._send_request(url, params)
        if not result.get("response") == "accepted":
            raise VenroTaskNotAccepted(f"VenroClientError, response={result}")
        return result

    async def _send_request(self, url, params: dict | None = None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, headers=self.headers, params=params
                ) as resp:
                    data = await resp.text()
            resp.raise_for_status()
            json_data = json.loads(data)
            error_message = json_data.get("error", "")
            if "api key" in error_message:
                raise VenroBadApiKey(error_message)
            elif "empty" in error_message:
                raise VenroNoTasks(error_message)
            elif "invalid access" in error_message:
                raise VenroInvalidAccess(error_message)
            elif "bot_id" in error_message:
                raise VenroInvalidBotId(error_message)
            elif "already sent" in error_message:
                raise VenroTaskAlreadySent(error_message)
            elif "incorrect task id" in error_message:
                raise VenroIncorrectTaskId(error_message)
            elif error_message:
                raise VenroClientError(f"VenroClientError, message: {error_message}")
            return json_data
        except JSONDecodeError as e:
            raise VenroClientError(f'JSONDecodeError {e}, "response = {data}"')
        except aiohttp.ClientHttpProxyError as e:
            raise e
        except aiohttp.ClientResponseError as e:
            raise VenroClientError(f'VenroClientError {e}, "response = {data}"')
