import asyncio
from dataclasses import dataclass

from dishka import Provider, make_async_container, Scope, from_context, provide


@dataclass
class WorkerId:
    value: str


class MyService:
    def __init__(self, worker_id: WorkerId):
        self.worker_id = worker_id


class MyProvider(Provider):
    scope = Scope.REQUEST
    worker_id = from_context(provides=WorkerId, scope=Scope.REQUEST)

    @provide
    def get_service(self, worker_id: WorkerId) -> MyService:
        return MyService(worker_id=worker_id)


async def main():
    provider = MyProvider()
    container = make_async_container(provider)

    async with container(context={WorkerId: WorkerId(value="1231213")}) as r_container:
        service = await r_container.get(MyService)
        print(service.worker_id)  # выведет "123e4567"

    async with container(context={WorkerId: WorkerId(value="ssssss")}) as r_container:
        service = await r_container.get(MyService)
        print(service.worker_id)  # выведет "123e4567"

asyncio.run(main())
