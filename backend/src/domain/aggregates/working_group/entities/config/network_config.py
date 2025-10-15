from pydantic import BaseModel, Field


class WorkingGroupNetworkConfig(BaseModel):
    max_network_wait_time: int = Field(
        default=15,
        ge=5,
        le=120,
        title="Макс. время ожидания сети",
        description="Максимальное время ожидания сетевого запроса в секундах",
    )
    retry_on_network_errors: bool = Field(
        default=True,
        title="Делать повторные попытки при ошибках соединения",
        description="Делать повторные попытки при ошибках соединения",
    )
    max_retries_on_network_errors: int = Field(
        default=0,
        ge=0,
        le=10,
        title="Макс. повторов при сетевых ошибках",
        description="Максимальное количество повторных попыток при сетевых ошибках",
    )

    delay_before_retries_on_network_errors: int = Field(
        default=0,
        ge=0,
        le=60,
        title="Задержка перед повтором",
        description="Задержка в секундах перед повторной попыткой при сетевой ошибке",
    )
    work_with_proxy: bool = Field(
        default=True,
        title="Использовать прокси",
        description="Использовать прокси для сетевых запросов",
    )
    max_accounts_per_proxy: int = Field(
        default=1,
        ge=1,
        le=100,
        title="Макс. аккаунтов на прокси",
        description="Максимальное количество аккаунтов на один прокси",
    )
    change_proxy_on_network_errors: bool = Field(
        default=True,
        title="Менять прокси при ошибках",
        description="Менять прокси при возникновении сетевых ошибок",
    )
    max_proxy_changes_on_network_errors: int = Field(
        default=1,
        ge=0,
        le=10,
        title="Макс. смен прокси",
        description="Максимальное количество смен прокси при сетевых ошибках",
    )
    delay_before_proxy_changes_on_network_errors: int = Field(
        default=1,
        ge=0,
        le=30,
        title="Задержка перед сменой прокси",
        description="Задержка в секундах перед сменой прокси при ошибке",
    )
