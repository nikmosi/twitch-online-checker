import asyncio
import sys

import httpx
from aiolimiter import AsyncLimiter

# 1 запрос в секунду
limiter = AsyncLimiter(1, 1)


async def is_twitch_live(
    nickname: str,
    client: httpx.AsyncClient,
    limiter: AsyncLimiter,
) -> tuple[str, bool, str]:
    url = f"https://decapi.me/twitch/uptime/{nickname}"

    async with limiter:
        response = await client.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/plain",
            },
        )

    response.raise_for_status()

    text = response.text.strip()
    lower = text.lower()

    if "offline" in lower:
        return nickname, False, text

    if "not found" in lower or "invalid" in lower or "error" in lower:
        raise ValueError(f"{nickname}: сервис вернул ошибку: {text}")

    return nickname, True, text


async def check_nickname(
    nickname: str,
    client: httpx.AsyncClient,
    limiter: AsyncLimiter,
) -> None:
    try:
        nickname, online, raw = await is_twitch_live(nickname, client, limiter)

        if online:
            print(f"{nickname}: ONLINE")
            print(f"Uptime: {raw}")
        else:
            print(f"{nickname}: OFFLINE")
            print(f"Ответ сервиса: {raw}")

    except Exception as e:
        print(f"{nickname}: Ошибка: {e}")


async def async_main():
    if len(sys.argv) < 2:
        print(
            "Использование: python twitch_check.py <nickname1> <nickname2> <nickname3>"
        )
        sys.exit(1)

    nicknames = sys.argv[1:]

    try:
        timeout = httpx.Timeout(15.0)
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            tasks = [
                check_nickname(nickname, client, limiter) for nickname in nicknames
            ]
            await asyncio.gather(*tasks)

    except Exception as e:
        print("Ошибка:", e)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(async_main())
