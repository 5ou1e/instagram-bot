import asyncio
import time
import os
import redis.asyncio as aioredis

NUM_WORKERS = 2000
NUM_LOGS_PER_WORKER = 100
LOG_MESSAGE = b"x" * 10
KEY = "logs"

WRITERS = os.cpu_count() or 4  # 4–16 обычно ок
MAX_CONN = 64  # пул коннектов


async def producer(q: asyncio.Queue):
    for _ in range(NUM_LOGS_PER_WORKER):
        await q.put(LOG_MESSAGE)


async def writer(r: aioredis.Redis, q: asyncio.Queue):
    while True:
        msg = await q.get()
        try:
            await r.lpush(KEY, msg)  # один LPUSH на msg
        finally:
            q.task_done()


async def main():
    r = aioredis.from_url(
        "redis://localhost",
        decode_responses=False,
        max_connections=MAX_CONN,  # важен пул
        health_check_interval=0,
    )

    q = asyncio.Queue(maxsize=NUM_WORKERS * 4)
    start = time.time()

    writers = [asyncio.create_task(writer(r, q)) for _ in range(WRITERS)]
    prods = [asyncio.create_task(producer(q)) for _ in range(NUM_WORKERS)]

    await asyncio.gather(*prods)
    await q.join()

    for w in writers: w.cancel()
    for w in writers:
        try:
            await w
        except asyncio.CancelledError:
            pass

    elapsed = time.time() - start
    total = NUM_WORKERS * NUM_LOGS_PER_WORKER
    print(f"Total ops: {total}, elapsed: {elapsed:.2f}s, throughput: {total / elapsed:.0f} ops/s")
    await r.aclose()


if __name__ == "__main__":
    asyncio.run(main())
