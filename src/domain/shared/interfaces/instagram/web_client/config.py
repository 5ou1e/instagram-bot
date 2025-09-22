from dataclasses import dataclass

from src.domain.proxy.entities import Proxy
from src.domain.user_agent.entities import UserAgent


@dataclass
class WebInstagramClientConfig:
    proxy: Proxy | None = None
    user_agent: UserAgent | None = None
    user_agent_mobile: UserAgent | None = None
    cookies: dict | None = None
