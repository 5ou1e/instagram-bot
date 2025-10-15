from pydantic import BaseModel, Field

from src.domain.aggregates.account_worker.entities.account_worker_log import LogLevel


class WorkingGroupLoggingConfig(BaseModel):
    enabled: bool = Field(
        default=True,
        title="Включить логирование",
        description="Включить или выключить логирование задачи",
    )
    level: LogLevel = Field(
        default=LogLevel.DEBUG,
        title="Уровень логирования",
        description="""
            "DEBUG": "DEBUG: Все сообщения включая отладочную информацию",
            "INFO": "INFO: Информационные сообщения и выше",
            "WARNING": "WARNING: Предупреждения и ошибки",
            "ERROR": "ERROR: Только ошибки",
        """,
    )
