import asyncio
import re
from typing import Union

import aiohttp
import zstandard as zstd
from aiohttp import ClientResponse
from orjson import orjson

from src.domain.shared.interfaces.instagram.entities.challenge import ChallengeData
from src.domain.shared.interfaces.instagram.exceptions import (
    BadRequestError,
    BadResponseError,
    ChallengeRequired,
    FeedbackRequiredError,
    InstagramError,
    LoginRequired,
    NetworkError,
    NotFoundError,
    OopsAnErrorOccurred,
    TooManyRequestsError,
)
from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.instagram.common.http_session import HttpSession
from src.infrastructure.instagram.mobile_client.requests.base.request import HttpRequest
from src.infrastructure.instagram.mobile_client.state import MobileInstagramClientState
from src.infrastructure.instagram.mobile_client.utils.extractors import (
    extract_data_from_authorization,
)

HEADER_MAPPINGS = {
    "ig-set-password-encryption-key-id": "public_key_id",
    "ig-set-password-encryption-pub-key": "public_key",
    "ig-set-x-mid": "mid",
    "ig-set-ig-u-ds-user-id": "user_id",
    "ig-set-ig-u-shbid": "shbid",
    "ig-set-ig-u-shbts": "shbts",
    "ig-set-ig-u-rur": "rur",
    "ig-set-ig-u-ig-direct-region-hint": "direct_region_hint",
    "ig-set-csrftoken": "csrf_token",
}


class RequestHandler:
    def __init__(
        self,
        client_state: MobileInstagramClientState,
        http_session: HttpSession,
        logger: Logger,
        max_retries: int = 0,
        delay_before_retry: float = 0.0,
    ):
        self._client_state = client_state
        self._http_session = http_session
        self.logger = logger
        self._max_retries = max_retries
        self._delay_before_retry = delay_before_retry
        self.dctx = zstd.ZstdDecompressor()

    async def __call__(
        self,
        request: HttpRequest,
    ) -> dict:
        # await self.logger.info(json.dumps(request.headers, indent=3))

        response, raw_content, elapsed_ms = await self._execute_request(request)

        self._update_client_state_after_success_response(
            response, raw_content, elapsed_ms
        )

        await self.logger.info(request.url)
        await self.logger.info(
            f"Сессионные данные после запроса: {self._client_state.local_data}"
        )

        if "zstd" in response.headers.get("Content-Encoding", ""):
            try:
                try:
                    # пробуем обычный метод
                    content = self.dctx.decompress(raw_content)
                except zstd.ZstdError:
                    # если не получилось — пробуем потоковый
                    import io

                    with self.dctx.stream_reader(io.BytesIO(raw_content)) as reader:
                        content = reader.read()
            except zstd.ZstdError as e:
                raise BadResponseError(
                    message=f"Не удалось декодировать zstd контент: {str(e)}"
                )
        else:
            content = raw_content

        try:
            data = orjson.loads(content)
        except Exception as e:
            print(e)
            try:
                data = content.decode("utf-8", errors="replace")
            except Exception as e:
                raise BadResponseError(message=f"Не удалось декодировать ответ в utf-8")

        await self._log_response(response, data)

        if response.status != 200:
            self.parse_and_raise_error(request, response, data)

        # if not isinstance(data, dict):
        #     raise InstagramError(message=f"Инстаграм сервер вернул не JSON")

        return data

    async def _execute_request(
        self, request
    ) -> tuple[aiohttp.ClientResponse, bytes, float]:
        """Выполняет HTTP-запрос с повторными попытками при сетевых ошибках"""

        for attempt in range(self._max_retries + 1):
            try:
                await self._log_request(request)

                headers = {k.lower(): v for k, v in request.headers.items()}
                request.headers = headers

                start = asyncio.get_event_loop().time()

                async with self._http_session.request(
                    request.method,
                    request.url,  # noqa
                    data=request.data,  # noqa
                    params=request.params,  # noqa
                    headers=request.headers,  # noqa
                    proxy=request.proxy or self._http_session.proxy,  # noqa
                ) as response:
                    content = await response.read()
                    elapsed_ms = int((asyncio.get_event_loop().time() - start) * 1000)
                    return response, content, elapsed_ms

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt < self._max_retries:
                    await self.logger.debug(
                        "Ошибка сети %d/%d: %s. Повторная попытка через %d секунд...",
                        attempt + 1,
                        self._max_retries + 1,
                        str(e),
                        self._delay_before_retry,
                    )
                    await asyncio.sleep(self._delay_before_retry)
                    continue

                raise NetworkError(
                    message=(
                        "Request timeout"
                        if isinstance(e, asyncio.TimeoutError)
                        else f"AiohttpClient error: {e}"
                    )
                ) from e

    async def _log_request(self, request: HttpRequest):
        """Логирует детали исходящего запроса"""

        await self.logger.debug(
            "Request: \n%s %s\nHeaders: %s\nCookies: %s\nData: %s\nProxy: %s",
            request.method,
            request.url,
            request.headers,
            request.headers.get("Cookie"),
            request.data,
            request.proxy or self._http_session.proxy,
        )

    async def _log_response(self, resp: ClientResponse, body: Union[str, dict] | None):
        """Логирует детали ответа"""
        # Ограничиваем размер лога и убираем проблемные символы

        body_str = re.sub(r"[\r\n]+", "", str(body)[:200])
        safe_body = "".join(c for c in body_str if ord(c) < 128)

        await self.logger.debug(
            "Response: \nStatus: %s\nHeaders: %s\nSet-Cookie: %s\nBody: %s",
            resp.status,
            resp.headers,
            resp.headers.get("Set-Cookie"),
            safe_body,
        )

    def _update_client_state_after_success_response(
        self, response: ClientResponse, raw_content, elapsed_time
    ):
        self._sync_session_data(response)
        self._client_state.increment_request_stats(
            len(raw_content) if raw_content else 0, elapsed_time
        )

    def _sync_session_data(self, response: ClientResponse) -> None:
        """Синхронизирует session_data с заголовками ответа"""

        for header_name, attr_name in HEADER_MAPPINGS.items():
            header_value = response.headers.get(header_name)

            if header_value and hasattr(self._client_state.local_data, attr_name):
                setattr(self._client_state.local_data, attr_name, header_value)

        authorization_header = response.headers.get("ig-set-authorization")

        if isinstance(authorization_header, str) and not authorization_header.endswith(
            ":"
        ):
            authorization_data = extract_data_from_authorization(authorization_header)
            self._client_state.local_data.set_authorization_data(authorization_data)

    def parse_and_raise_error(
        self,
        request: HttpRequest,
        response: aiohttp.ClientResponse,
        data: Union[dict, str],
    ) -> None:
        status = response.status
        if isinstance(data, dict):
            message = data.get("message", "").lower()

            err_message = message + " | " + f"Request endpoint: {request.url}"
            if status == 400:
                if "challenge_required" in message:
                    challenge_data = data.get("challenge", {})
                    raise ChallengeRequired(
                        challenge_data=ChallengeData.model_validate(challenge_data),
                        message=str(data),
                    )
                if "feedback_required" in message:
                    raise FeedbackRequiredError(
                        message=str(data),
                    )
                raise BadRequestError(message=err_message)
            if status == 403:
                if "login_required" in message:
                    raise LoginRequired(
                        message=message + " | " + f"Request endpoint: {request.url}"
                    )
                raise InstagramError(
                    message=message + " | " + f"Request endpoint: {request.url}"
                )
            if status == 404:
                if "payload returned is null" in message:
                    raise InstagramError(
                        message=message + " | " + f"Request endpoint: {request.url}"
                    )
                raise NotFoundError(message=err_message)
            if status == 429:
                raise TooManyRequestsError(message=err_message)

            raise InstagramError(
                message=f"status: {status} | "
                + message
                + " | "
                + f"Request endpoint: {request.url}"
            )

        else:
            short_body = re.sub(r"[\r\n]+", "", data[:200])

            if "oops, an error occurred" in data.lower():
                raise OopsAnErrorOccurred()

            if status == 404:
                raise NotFoundError(message=short_body)

            raise InstagramError(
                message=f"Status: {status} | "
                + short_body
                + " | "
                + f"Request endpoint: {request.url}"
            )
