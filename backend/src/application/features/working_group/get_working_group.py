import logging
from uuid import UUID

from src.application.common.dtos.working_group import WorkingGroupDTO
from src.application.common.interfaces.working_group_reader import WorkingGroupReader

logger = logging.getLogger(__name__)


class GetWorkingGroupQueryHandler:

    def __init__(
        self,
        reader: WorkingGroupReader,
    ):
        self._reader = reader

    async def __call__(
        self,
        working_group_id: UUID,
    ) -> WorkingGroupDTO:
        return await self._reader.get_working_group_by_id(working_group_id)
