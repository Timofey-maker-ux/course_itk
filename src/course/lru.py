import functools
import unittest.mock
from collections import OrderedDict
from typing import Any, Callable


def lru_cache(func: Callable | None = None, *, maxsize: int | None = None):
    def decorator(fn: Callable):
        cache = OrderedDict()

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any):
            key = (args, frozenset(kwargs.items()))

            if key in cache:
                cache.move_to_end(key)
                return cache[key]

            result = fn(*args, **kwargs)
            cache[key] = result
            cache.move_to_end(key)

            if maxsize is not None and len(cache) > maxsize:
                cache.popitem(last=False)

            return result

        return wrapper

    if func is not None and callable(func):
        return decorator(func)

    return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
