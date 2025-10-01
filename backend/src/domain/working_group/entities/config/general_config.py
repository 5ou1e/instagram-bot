from pydantic import BaseModel, Field


class WorkingGroupGeneralConfig(BaseModel):
    max_parallel_processing_accounts_count: int = Field(
        default=100,
        ge=1,
        le=1000,
        title="Макс. одновременно работающих аккаунтов",
        description="Макс. одновременно работающих аккаунтов",
    )
    delay_before_start_new_account: int = Field(
        default=0,
        ge=0,
        le=300,
        title="Задержка между запуском аккаунтов",
        description="Задержка в секундах перед запуском нового аккаунта",
    )
    wait_for_new_accounts_if_all_processed: bool = Field(
        default=True,
        title="Ожидать новые аккаунты",
        description="Ожидать появления новых аккаунтов после обработки всех",
    )
