
def to_snake_case(name):
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")

class InjectableMeta(type):
    __instances__ = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances__:
            cls.__instances__[cls] = super().__call__(*args, **kwargs)
        instance = cls.__instances__[cls]
        for attr in cls.__inject__:
            setattr(instance, to_snake_case(attr.__name__), attr())
        return instance
    def __new__(cls, name, bases, dct):
        if "__inject__" not in dct:
            dct["__inject__"] = []
        return super().__new__(cls, name, bases, dct)
    @classmethod
    def reset(cls, target: type=None):
        del cls.__instances__[target]
    @classmethod
    def reset_all(cls):
        cls.__instances__ = {}

class ConsumerMeta(type):
    def __new__(cls, name, bases, dct):
        if "__inject__" not in dct:
            dct["__inject__"] = []
        return super().__new__(cls, name, bases, dct)
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        for attr in cls.__inject__:
            setattr(instance, to_snake_case(attr.__name__), attr())
        return instance

class Injectable(metaclass=InjectableMeta):
    ...

class Consumer(metaclass=ConsumerMeta):
    ...
