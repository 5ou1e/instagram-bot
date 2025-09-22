import asyncio

import aiofiles


class File:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._lock = asyncio.Lock()

    async def write(self, line: str) -> None:
        async with self._lock:
            # открываем только для дозаписи
            async with aiofiles.open(self._filepath, mode="a", encoding="utf-8") as f:
                await f.write(line + "\n")
