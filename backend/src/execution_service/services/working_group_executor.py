from uuid import UUID


class WorkingGroupExecutor:
    """Асинхронный обработчик выполнения задачи рабочей группы, с возможностью старт\стоп"""

    def __init__(self):
        pass

    def start(self, task_account_id: UUID):
        """Запустить рабочую группу"""

    def stop(self, task_account_id: UUID):
        """Остановить рабочую группу"""
