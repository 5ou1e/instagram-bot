from yarl import URL

from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common import constants
from src.infrastructure.instagram.common.utils import build_signed_body, dumps_orjson
from src.infrastructure.instagram.mobile_client.requests.base.headers_factory import (
    MobileInstagramClientHeadersFactory,
)
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.requests.base.request_handler import (
    RequestHandler,
)
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState


class LiveSection:

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

    async def get_good_time_for_live(self):

        uri = constants.NEWS_INBOX_URI
        url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        headers = MobileInstagramClientHeadersFactory.bloks_headers(
            self._device_info,
            self._version_info,
            self._local_data,
        )

        headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Ig-Client-Endpoint": "MainFeedFragment:feed_timeline",
                "X-Fb-Friendly-Name": f"IgApi: {uri}",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=3",
                "x-fb-rmd": "state=URL_ELIGIBLE",
                "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755691661.66:::1755691661.66",
            }
        )

        data = {
            "_uid": self._local_data.user_id,
            "_uuid": self._local_data.device_id,
        }
        signed_data = build_signed_body(dumps_orjson(data))

        request = HttpRequest(
            method="GET",
            url=url,
            headers=headers,
            data=signed_data,
        )

        response = await self._request_handler(request)

        return response
