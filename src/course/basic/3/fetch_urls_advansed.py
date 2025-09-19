import asyncio
import json

import aiofiles
import aiohttp


async def fetch_urls(input_file: str, output_file: str) -> None:
    semaphore = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:

        async def fetch(url: str) -> dict | None:
            async with semaphore:
                try:
                    async with session.get(url, timeout=60) as response:
                        if response.status == 200:
                            data = await response.json()
                            return {url: data}
                        return None
                except aiohttp.ClientConnectorError:
                    return {url: 0}  # ошибка соединения
                except asyncio.TimeoutError:
                    return {url: -1}  # таймаут
                except aiohttp.InvalidURL:
                    return {url: -2}  # ошибка url
                except Exception:
                    return {url: -99}  # остальные ошибки

        urls = []
        async with aiofiles.open(input_file, "r", encoding="utf-8") as f:
            async for line in f:
                line = line.strip()
                if line:
                    urls.append(line)

        tasks = [fetch(url) for url in urls]

        async with aiofiles.open(output_file, "w", encoding="utf-8") as f:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                if result:
                    await f.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    asyncio.run(fetch_urls("urls.txt", "result.jsonl"))
