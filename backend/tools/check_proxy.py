# vk_direct_proxy.py
import asyncio
import aiohttp

# ПРОКСИ ПОДСТАВЛЕНО ТОЧНО ТАК, КАК ДАЛИ (без разбора)
PROXY_RAW = "xVqj79:YQAJMe@185.240.95.33:8000"
PROXY = "http://" + PROXY_RAW  # aiohttp ожидает URL-like строку, поэтому добавляем http://
URL = "https://instagram.com"


async def main():
    timeout = aiohttp.ClientTimeout(total=20)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"}

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(URL, headers=headers) as resp:
                print("Status:", resp.status)
                body = await resp.text(errors="replace")
                print(body[:800])  # печатаем первые 800 символов ответа
        except Exception as e:
            print("Request error:", repr(e))


if __name__ == "__main__":
    asyncio.run(main())
