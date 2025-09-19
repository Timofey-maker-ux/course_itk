import redis
import time
import random


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, name: str = "api", max_requests=5, window=3,
                 host="localhost", port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)
        self.key = f"rate_limit:{name}"
        self.max_requests = max_requests
        self.window = window

    def test(self) -> bool:
        now = time.time()
        pipe = self.r.pipeline()

        pipe.zremrangebyscore(self.key, 0, now - self.window)

        pipe.zadd(self.key, {str(now): now})

        pipe.zcard(self.key)

        pipe.expire(self.key, self.window)

        _, _, count, _ = pipe.execute()

        return count <= self.max_requests


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # бизнес-логика
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
