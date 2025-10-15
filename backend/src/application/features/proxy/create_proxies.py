import logging
from dataclasses import dataclass
from uuid import UUID

from src.application.common.converters.proxy import convert_proxy_line_to_entity
from src.domain.aggregates.proxy.repository import ProxyRepository
from src.domain.shared.interfaces.uow import Uow

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, slots=True)
class CreateProxiesCommandResult:
    ids: list[UUID]


class CreateProxiesCommandHandler:

    def __init__(
        self,
        uow: Uow,
        repository: ProxyRepository,
    ):
        self._uow = uow
        self._repository = repository

    async def __call__(
        self,
        data: list[str],
    ) -> CreateProxiesCommandResult:
        async with self._uow:
            entities = [convert_proxy_line_to_entity(line) for line in data]
            created_proxies = await self._repository.bulk_create(
                entities,
                on_conflict_do_nothing=True,
            )
            return CreateProxiesCommandResult(
                ids=[proxy.id for proxy in created_proxies],
            )
