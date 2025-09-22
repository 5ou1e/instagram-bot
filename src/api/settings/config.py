from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str
    min_size: int = 10  # Минимальное количество соединений в пуле
    max_size: int = (
        100  # Максимальное количество соединений, которые могут быть "переполнены"
    )

    @property
    def url_sa(self) -> str:
        # URL для SQLAlchemy (asyncpg)
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class CORSConfig(BaseModel):
    allowed_hosts: list[str]


class ApiV1Config(BaseModel):
    prefix: str = "/v1"


class ApiConfig(BaseModel):
    url: str
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()
    cors: CORSConfig


class LogsConfig(BaseModel):
    root_dir: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="",
    )
    db: DatabaseConfig
    api: ApiConfig
    logs: LogsConfig


config: Config = Config()
