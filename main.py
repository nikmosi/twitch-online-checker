import asyncio
import sys

import httpx
from aiolimiter import AsyncLimiter

# Настрой лимит под свои нужды
limитер = AsyncLimiter(1, 1)  # 1 запрос в 1 секунду


async def is_twitch_live(
    nickname: str,
    client: httpx.AsyncClient,
    limiter: AsyncLimiter,
) -> tuple[bool, str]:
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
        return False, text

    if "not found" in lower or "invalid" in lower or "error" in lower:
        raise ValueError(f"Сервис вернул ошибку: {text}")

    return True, text


async def async_main():
    if len(sys.argv) < 2:
        print("Использование: python twitch_check.py <nickname>")
        sys.exit(1)

    nickname = sys.argv[1]

    try:
        timeout = httpx.Timeout(15.0)
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            online, raw = await is_twitch_live(nickname, client, лимитер)

        if online:
            print(f"{nickname}: ONLINE")
            print(f"Uptime: {raw}")
        else:
            print(f"{nickname}: OFFLINE")
            print(f"Ответ сервиса: {raw}")

    except Exception as e:
        print("Ошибка:", e)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(async_main())
