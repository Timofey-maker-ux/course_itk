from datetime import datetime


class AutoCreatedAtMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=AutoCreatedAtMeta):
    pass


if __name__ == "__main__":
    obj = MyClass()
    print(f"obj created_at: {obj.created_at}")
    assert hasattr(obj, "created_at")
    assert isinstance(obj.created_at, datetime)
