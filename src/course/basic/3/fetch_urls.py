import asyncio
import json

import aiofiles
import aiohttp


async def fetch_urls(urls: list[str], file_path: str) -> None:
    semaphore = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:

        async def fetch(url: str) -> dict:
            async with semaphore:
                try:
                    async with session.get(url, timeout=10) as response:
                        return {url: response.status}
                except aiohttp.ClientConnectorError:
                    return {url: 0}  # ошибка соединения
                except asyncio.TimeoutError:
                    return {url: -1}  # таймаут
                except aiohttp.InvalidURL:
                    return {url: -2}  # ошибка url
                except Exception:
                    return {url: -99}  # остальные ошибки

        results = await asyncio.gather(*[fetch(url) for url in urls])

        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            for result in results:
                await f.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url",
    ]
    asyncio.run(fetch_urls(urls, "./results.jsonl"))
