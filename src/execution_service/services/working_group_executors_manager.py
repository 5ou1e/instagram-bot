from uuid import UUID

from src.execution_service.services.working_group_executor import WorkingGroupExecutor


class WorkingGroupExecutorsManager:
    """
    Обьект управляющий запусками\остановками задач рабочих групп
    Хранит обьекты WorkingGroupExecutors, под каждую запущенную р.г.
    """

    def __init__(self):
        self._working_group_executors = {}

    async def start_working_group(self, working_group_id: UUID):
        self._working_group_executors[working_group_id] = WorkingGroupExecutor(
            working_group_id
        )

    async def stop_working_group(self, working_group_id: UUID):
        pass
