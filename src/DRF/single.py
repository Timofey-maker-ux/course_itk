import functools
import uuid
import datetime

import redis

r = redis.Redis(host="localhost", port=6379, db=0)

def single(max_processing_time: datetime.timedelta):

    def decorator(func):
        lock_key = f"single_lock:{func.__name__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_id = str(uuid.uuid4())
            acquired = r.set(
                lock_key,
                lock_id,
                nx=True,
                ex=int(max_processing_time.total_seconds()),
            )

            if not acquired:
                raise RuntimeError(f"Функция {func.__name__} уже выполняется")

            try:
                return func(*args, **kwargs)
            finally:
                if r.get(lock_key) == lock_id.encode():
                    r.delete(lock_key)

        return wrapper

    return decorator
