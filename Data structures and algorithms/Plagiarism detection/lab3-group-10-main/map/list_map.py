
from .map import Map, Key, Value


class ListMap(Map[Key, Value]):
    """
    Map implemented as a list of pairs `(key, values)`.
    This is a very stupid idea and should not be used in practice!
    """
    kvpairs: list[tuple[Key, Value]]

    def __init__(self):
        self.kvpairs = []

    def size(self) -> int:
        return len(self.kvpairs)

    def get(self, key: Key) -> Value | None:
        if key is None: # type: ignore
            raise ValueError("Key is None")
        for key_, value in self.kvpairs:
            if key == key_:
                return value
        return None

    def put(self, key: Key, value: Value):
        if key is None: # type: ignore
            raise ValueError("Key is None")
        if value is None:
            raise ValueError("Value is None")
        for i, (key_, _value) in enumerate(self.kvpairs):
            if key == key_:
                self.kvpairs[i] = (key_, value)
                return
        self.kvpairs.append((key, value))

    def clear(self):
        self.kvpairs.clear()

    def keys(self) -> tuple[Key, ...]:
        return tuple(key for key, _ in self.kvpairs)

    ###########################################################################
    # Validation

    def validate(self):
        keyset = set(self)
        assert len(keyset) == len(self), "Duplicate keys"
        for key, value in self.kvpairs:
            assert key is not None, "Key is None"
            assert value is not None, "Value is None"


