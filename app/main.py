from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from .worker import add, celery

app = FastAPI()
engine = create_async_engine("mysql+aiomysql://root:root@mysql:3306")


@app.get(
    "/hello",
    summary="Return a hello message",
    description="""
        An example of serving multiple concurrent requests by 
        performing non-blocking database calls
        """
)
async def hello(name: str):
    message = await get_welcome_message()
    return f"{message} {name}"


async def get_welcome_message() -> str:
    async with engine.connect() as conn:
        # simulate a long running query
        result = await conn.execute(text("SELECT 'Hello' as message, SLEEP(1)"))
    return result.fetchone()[0]


@app.post(
    "/add",
    summary="Create a celery task that returns the sum of 2 numbers",
    description="""
        An example of serving multiple requests in a non-blocking fashion by offloading 
        some dummy cpu-intensive calculation to a task queue
        """
)
def create_add_task(n1: int, n2: int):
    task = add.delay(n1, n2)
    return {"task_id": task.id,
            "n1": n1,
            "n2": n2}


@app.get(
    "/add/{task_id}",
    summary="Get status of a celery task by id",
    description="""
        Returns the status of the celery tasks and its
        result if completed
    """
)
def get_task_status(task_id: str):
    task_result = celery.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
