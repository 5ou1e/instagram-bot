import logging

from src.application.common.dtos.working_group import WorkingGroupsDTO
from src.application.common.interfaces.working_group_reader import WorkingGroupReader

logger = logging.getLogger(__name__)


class GetWorkingGroupsQueryHandler:

    def __init__(
        self,
        reader: WorkingGroupReader,
    ):
        self._reader = reader

    async def __call__(
        self,
    ) -> WorkingGroupsDTO:
        return await self._reader.get_working_groups()
