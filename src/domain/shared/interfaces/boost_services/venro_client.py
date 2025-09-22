from asyncio import Protocol
from dataclasses import dataclass

from mashumaro import DataClassDictMixin


@dataclass(kw_only=True, slots=True)
class VenroTaskData(DataClassDictMixin):
    id: str
    item_id: str
    item_type: str
    code: str
    type: str
    money: str


class VenroClient(Protocol):

    async def get_task_follow(self, api_key, bot_id, service_id) -> VenroTaskData: ...

    async def get_task_like(self, api_key, bot_id, service_id) -> VenroTaskData: ...

    async def get_task_comment(self, api_key, bot_id, service_id) -> VenroTaskData: ...

    async def get_task(self, api_key, bot_id, service_id) -> VenroTaskData: ...

    async def send_task_done(
        self, api_key, working_group_id, bot_id, bot_username
    ) -> dict:
        """Отправляем на проверку"""
        ...

    async def send_task_cancel(self, api_key, working_group_id) -> dict:
        """Отмена задания"""
        ...
