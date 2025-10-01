import aiohttp
from aiohttp import ClientSession, ClientTimeout

from src.domain.proxy.entities import Proxy
from src.domain.shared.interfaces.instagram.mobile_client.client import (
    MobileInstagramClient,
)
from src.domain.shared.interfaces.instagram.mobile_client.config import (
    MobileInstagramClientNetworkConfig,
)
from src.domain.shared.interfaces.instagram.mobile_client.entities.android_device_info import (
    MobileClientAndroidDeviceInfo,
)
from src.domain.shared.interfaces.instagram.mobile_client.entities.local_data import (
    MobileInstagramClientLocalData,
)
from src.domain.shared.interfaces.instagram.version import InstagramAppVersion
from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common.http_session import HttpSession
from src.infrastructure.instagram.mobile_client.instagram_version_info import (
    VersionInfoRegistry,
)
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.sections.auth import AuthSection
from src.infrastructure.instagram.mobile_client.sections.direct import DirectSection
from src.infrastructure.instagram.mobile_client.sections.feed import FeedSection
from src.infrastructure.instagram.mobile_client.sections.launcher import LauncherSection
from src.infrastructure.instagram.mobile_client.sections.live import LiveSection
from src.infrastructure.instagram.mobile_client.sections.media import MediaSection
from src.infrastructure.instagram.mobile_client.sections.news import NewsSection
from src.infrastructure.instagram.mobile_client.sections.notifications import (
    NotificationsSection,
)
from src.infrastructure.instagram.mobile_client.sections.test_auth import (
    TestAuthSection,
)
from src.infrastructure.instagram.mobile_client.sections.user import UserSection
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class MobileInstagramClientImpl(MobileInstagramClient):

    def __init__(
        self,
        version: InstagramAppVersion,
        logger: Logger,
        device_info: MobileClientAndroidDeviceInfo | None = None,
        local_data: MobileInstagramClientLocalData | None = None,
        network_config: MobileInstagramClientNetworkConfig | None = None,
    ):
        self._state = MobileInstagramClientState(
            device_info=device_info or MobileClientAndroidDeviceInfo(),
            local_data=local_data or MobileInstagramClientLocalData.create(),
            version_info=VersionInfoRegistry.get(version),
        )
        self.logger = logger
        self.version = version
        self._network_config = network_config
        self._http_session = self._create_http_session()
        self._request_handler = RequestHandler(
            client_state=self._state,
            http_session=self._http_session,
            logger=logger,
            max_retries=network_config.max_retries_on_network_errors,
            delay_before_retry=network_config.delay_before_retries_on_network_errors,
        )
        self._init_sections()

    def _init_sections(self):
        section_context = {
            "state": self._state,
            "request_handler": self._request_handler,
            "logger": self.logger,
        }

        self.auth = AuthSection(**section_context)
        self.user = UserSection(**section_context)
        self.feed = FeedSection(**section_context)
        self.direct = DirectSection(**section_context)
        self.launcher = LauncherSection(**section_context)
        self.notifications = NotificationsSection(**section_context)
        self.news = NewsSection(**section_context)
        self.media = MediaSection(**section_context)
        self.live = LiveSection(**section_context)
        self.test_auth = TestAuthSection(**section_context)

    def _create_http_session(self) -> HttpSession:

        return HttpSession(
            aiohttp_session=ClientSession(
                timeout=ClientTimeout(total=self._network_config.max_network_wait_time),
                cookie_jar=aiohttp.DummyCookieJar(),  # Отключает автоматическую обработку кук
            ),
            proxy=self._network_config.proxy,
        )

    async def close(self):
        await self._http_session.close()

    async def __aenter__(self) -> "MobileInstagramClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._http_session.close()

    def set_proxy(self, proxy: Proxy) -> None:
        self._http_session.set_proxy(proxy)

    def get_local_data(self) -> MobileInstagramClientLocalData:
        return self._state.local_data
