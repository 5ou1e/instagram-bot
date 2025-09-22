from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from yarl import URL


@dataclass(kw_only=True, slots=True)
class HttpRequest:
    method: str
    url: str | URL
    headers: Dict[str, str] = field(default_factory=dict)
    data: Optional[Any] = None
    params: Optional[Dict[str, str]] = None
    json: Optional[Dict[str, Any]] = None
    proxy: Optional[str] = None
    cookies: Optional[dict] = None
