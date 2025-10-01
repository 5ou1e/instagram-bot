from .account import router as account_router
from .android_devices import router as android_devices_router
from .default.docs import router as docs_router
from .default.root import router as root_router
from .imap import router as imap_router
from .log import router as log_router
from .proxy import router as proxy_router
from .working_group import router as tasks_router

__all__ = [
    "root_router",
    "docs_router",
    "account_router",
    "imap_router",
    "proxy_router",
    "android_devices_router",
    "log_router",
    "tasks_router",
]
