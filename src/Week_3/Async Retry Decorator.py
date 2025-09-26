import asyncio
import functools


def async_retry(retries=3, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    count += 1
                    if count > retries:
                        raise
                    print(f"Retrying {func.__name__} ({count}/{retries})...")
                    await asyncio.sleep(0)
        return wrapper
    return decorator

if __name__ == '__main__':
    @async_retry(retries=3, exceptions=(ValueError,))
    async def unstable_task():
        print("Running task...")
        raise ValueError("Something went wrong")


    async def main():
        try:
            await unstable_task()
        except Exception as e:
            print(f"Final failure: {e}")


    asyncio.run(main())