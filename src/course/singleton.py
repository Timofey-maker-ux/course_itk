class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonWithMeta(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value


class SingletonWithNew:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        if not hasattr(self, "_initialized"):
            self.value = value
            self._initialized = True


if __name__ == "__main__":
    # Singleton с метаклассом
    a = SingletonWithMeta(10)
    b = SingletonWithMeta(20)
    assert a is b
    assert b.value == 10

    # Singleton через __new__
    c = SingletonWithNew(30)
    d = SingletonWithNew(40)
    assert c is d
    assert d.value == 30

    # Singleton через импорт
    from singleton_module import singleton_instance as s1
    from singleton_module import singleton_instance as s2
    assert s1 is s2
    assert s2.value == 100
