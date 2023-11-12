import time


def async_time_it(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time} seconds to run.")

    return wrapper
