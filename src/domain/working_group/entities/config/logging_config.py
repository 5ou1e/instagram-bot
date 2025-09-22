from pydantic import BaseModel, Field

from src.domain.account.entities.account_log import AccountWorkerLogLevel


class WorkingGroupLoggingConfig(BaseModel):
    enabled: bool = Field(
        default=True,
        title="Включить логирование",
        description="Включить или выключить логирование задачи",
    )
    level: AccountWorkerLogLevel = Field(
        default=AccountWorkerLogLevel.DEBUG,
        title="Уровень логирования",
        description="""
            "DEBUG": "DEBUG: Все сообщения включая отладочную информацию",
            "INFO": "INFO: Информационные сообщения и выше",
            "WARNING": "WARNING: Предупреждения и ошибки",
            "ERROR": "ERROR: Только ошибки",
        """,
    )
