from src.domain.account_worker.entities.account_worker.entity import AccountWorker
from src.domain.account_worker.services.actions.base import AccountWorkerActionExecutor



class AuthorizeAccountActionExecutor(AccountWorkerActionExecutor):
    def __init__(self):
        pass

    async def execute(self, worker: AccountWorker):
        return None


class FollowUserActionExecutor(AccountWorkerActionExecutor):
    def __init__(self):
        pass

    async def execute(self, worker: AccountWorker):
        return None


class ChangeProxyActionExecutor(AccountWorkerActionExecutor):
    def __init__(self):
        pass

    async def execute(self, worker: AccountWorker):
        return None


class Pipeline:

    def __init__(
        self,
        on_unauthorized = None,
        on_proxy_error = None,
    ):
        self._on_unauthorized = on_unauthorized
        self._on_proxy_error = on_proxy_error

    def execute(self, action):
        pass


# shell/middleware.py
from typing import Awaitable, Callable, Iterable
import asyncio, time

Exec = Callable[[Iterable[Command]], Awaitable[None]]  # базовый исполнителль
Middleware = Callable[[Exec], Exec]


def chain(middlewares: list[Middleware], endpoint: Exec) -> Exec:
    h = endpoint
    for mw in reversed(middlewares):
        h = mw(h)
    return h


def with_retry(attempts: int, delay: float, retry_on: tuple[type[Exception], ...]) -> Middleware:
    def mw(next_exec: Exec) -> Exec:
        async def wrapped(commands):
            tries = 0
            while True:
                try:
                    await next_exec(commands)
                    return
                except retry_on as e:
                    tries += 1
                    if tries >= attempts:
                        raise
                    await asyncio.sleep(delay)

        return wrapped

    return mw


def with_timeout(seconds: float) -> Middleware:
    def mw(next_exec: Exec) -> Exec:
        async def wrapped(commands):
            await asyncio.wait_for(next_exec(commands), timeout=seconds)

        return wrapped

    return mw


def pipeline():
    auth = AuthorizeAccountActionExecutor()
    change_proxy = ChangeProxyActionExecutor()
    follow = FollowUserActionExecutor()

    try:
        follow.execute()
    except
    except Unauthorized as e:
        auth.execute()
