from src.domain.aggregates.proxy.entities import Proxy
from src.infrastructure.database.repositories.proxy import PostgresProxyRepository


class ProxyProvider:
    # TODO рефакторинг
    def __init__(self, session_factory, max_usage_per_proxy: int = 500):
        self._session_factory = session_factory
        self._max_usage = 1

    async def _can_acquire_proxy(self, proxy: Proxy) -> bool:
        return proxy.usage < self._max_usage

    async def acquire(self) -> Proxy | None:
        async with self._session_factory() as session:
            try:
                repository = PostgresProxyRepository(session)

                proxy = await repository.acquire_least_used()
                if proxy and await self._can_acquire_proxy(proxy):
                    proxy.usage += 1
                    await repository.update(proxy)
                    await session.commit()
                    return proxy
                else:
                    await session.rollback()
                    return None
            except Exception as e:
                await session.rollback()
                raise

    async def release(self, proxy: Proxy) -> None:
        async with self._session_factory() as session:
            try:
                repository = PostgresProxyRepository(session)
                if proxy.usage > 0:
                    proxy.usage -= 1
                await repository.update(proxy)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise
