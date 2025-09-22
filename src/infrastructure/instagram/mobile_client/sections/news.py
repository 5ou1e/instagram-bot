from yarl import URL

from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.generators import utc_timezone_offset
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class NewsSection:

    def __init__(
        self,
        state: MobileInstagramClientState,
        request_handler: RequestHandler,
        logger: Logger,
    ):
        self._state = state
        self._request_handler = request_handler
        self.logger = logger

        self._device_info = self._state.device_info
        self._local_data = self._state.local_data
        self._version_info = self._state.version_info

    async def news_inbox(self):
        uri = constants.NEWS_INBOX_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "X-Ig-Client-Endpoint": "com.bloks.www.caa.login.login_homepage",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
                "x-fb-rmd": "state=URL_ELIGIBLE",
                "x-ig-304-eligible": "true",
                "x-ig-prefetch-request": "foreground",
            }
        )

        params = {
            "could_truncate_feed": "true",
            "should_skip_su": "false",
            "mark_as_seen": "false",
            "timezone_offset": utc_timezone_offset(self._device_info.timezone),
            "timezone_name": "Europe/Moscow",
        }

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            params=params,
        )

        response = await self._request_handler(request)

        return response
