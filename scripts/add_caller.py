import asyncio
import random
import time

import httpx

from utils import async_time_it


async def post_addition(client, n1: int, n2: int) -> dict:
    response = await client.post("http://127.0.0.1:80/add",
                                 params={"n1": n1, "n2": n2})
    return response.json()


async def get_result(client, task_id: str) -> dict:
    response = await client.get(f"http://127.0.0.1:80/add/{task_id}")
    return response.json()


@async_time_it
async def main():
    async with httpx.AsyncClient() as client:
        tasks = [post_addition(client, i, i) for i in range(10)]
        task_ids = await asyncio.gather(*tasks)
        print(task_ids)
        random_task_id = task_ids[random.randint(0, len(task_ids) - 1)]["task_id"]
        tasks_status = "PENDING"
        print(f"Starting ping for results of task with id {random_task_id}")
        while tasks_status == "PENDING":
            time.sleep(1)
            res = httpx.get(f"http://127.0.0.1:80/add/{random_task_id}")
            task_payload = res.json()
            print(task_payload)
            tasks_status = task_payload["task_status"]


if __name__ == "__main__":
    asyncio.run(main())
