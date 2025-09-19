import redis
import json


class RedisQueue:
    def __init__(self, name: str = "queue", host="localhost", port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)
        self.key = f"redis_queue:{name}"

    def publish(self, msg: dict):
        data = json.dumps(msg)
        self.r.rpush(self.key, data)

    def consume(self) -> dict | None:
        data = self.r.lpop(self.key)
        if data is None:
            return None
        return json.loads(data)


if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
