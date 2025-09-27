import aiohttp
import asyncio


async def fetch_instagram():
    proxy_host = "pr.oxylabs.io"
    proxy_port = "7777"
    proxy_user = "customer-ozan_zone10-sesstime-30-sessid-7SNWUVSj"
    proxy_pass = "38KZPLp0"

    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://www.vk.com/", proxy=proxy_url,
                                   timeout=10) as resp:
                print("Status:", resp.status)
                text = await resp.text()
                print(text[:500])  # печатаем первые 500 символов HTML
        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    asyncio.run(fetch_instagram())
