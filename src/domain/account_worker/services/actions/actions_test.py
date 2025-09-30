import asyncio
from dataclasses import dataclass
from functools import partial
from typing import Callable


class Unauthorized(Exception):
    pass


class Client:
    def authorize(self):
        pass

    def follow(self):
        raise Unauthorized(f"Unauthorized")


@dataclass(kw_only=True)
class OnErrorPolicy:
    retry: bool = True
    retries_count: int = 1
    calls_before: list[Callable]


class InstagramAction:
    pass

    async def execute(self, worker):
        ...


class AuthorizeAction(InstagramAction):

    def __init__(self, error_policies: dict[any, OnErrorPolicy] = {}):
        self.error_policies = error_policies

    async def execute(self, worker):
        client = Client()
        client.authorize()


class FollowAction(InstagramAction):

    def __init__(self, error_policies: dict[any, OnErrorPolicy] = {}):
        self.error_policies = error_policies
        self.error_policies_retries = {
            Unauthorized: 0,
        }

    async def execute(self, worker):
        client = Client()
        while True:
            try:
                client.follow()
            except Exception as e:
                print(e)
                error_policy = self.error_policies.get(type(e))
                if error_policy:
                    for call in error_policy.calls_before:
                        await call()
                    if error_policy.retry:
                        counter = self.error_policies_retries.get(type(e))
                        if counter >= error_policy.retries_count:
                            raise
                        self.error_policies_retries[type(e)]+= 1
                        continue

                raise e


async def main():
    worker_ = "Worker"
    follow = FollowAction(
        error_policies={
            Unauthorized: OnErrorPolicy(
                retry=True,
                retries_count=0,
                calls_before=[partial(AuthorizeAction().execute, worker_)]
            )
        }
    )
    await follow.execute(worker_)


asyncio.run(main())
