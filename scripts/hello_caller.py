import asyncio

import httpx

from utils import async_time_it

NAMES = ["Ted", "Barney", "Marshall", "Lilly", "Robin"]


async def get_hello_message(client, name) -> str:
    response = await client.get("http://127.0.0.1:80/hello",
                                params={"name": name})
    return response.json()


@async_time_it
async def main():
    async with httpx.AsyncClient() as client:
        tasks = [get_hello_message(client, name) for name in NAMES]
        res = await asyncio.gather(*tasks)
        print(res)


if __name__ == "__main__":
    asyncio.run(main())
