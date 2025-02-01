from typing import TypeVar, Generic
from collections.abc import Iterable, Iterator, Sequence
from types import EllipsisType

from .map import Map, Key, ComparableProtocol
Value = TypeVar('Value', bound=ComparableProtocol)


###############################################################################
# Simple multimaps

class Multimap(Iterable[Key], Generic[Key, Value]):
    """
    A class of simple multimaps (dictionaries mapping to sets of values).
    """

    # We use Ellipsis (...) as the value of the inner map,
    # because it is the smallest Python object that is not None.
    main_map: Map[Key, Map[Value, EllipsisType]]
    values_constructor: type[Map[Value, EllipsisType]]

    def __init__(self, map_constructor: type[Map[Key, Map[Value, EllipsisType]]],
                 values_constructor: type[Map[Value, EllipsisType]]):
        self.main_map = map_constructor()
        self.values_constructor = values_constructor

    def __len__(self) -> int:
        """Returns the number of keys."""
        return self.size()

    def size(self) -> int:
        return self.main_map.size()

    def contains(self, key: Key, value: Value) -> bool:
        values = self.main_map.get(key)
        assert values is not None, "Internal error: multimap values must not be None"
        return values.contains_key(value)

    def get_values(self, key: Key) -> Sequence[Value]:
        values = self.main_map.get(key)
        if values is None: return ()
        return values.keys()

    def add_value(self, key: Key, value: Value):
        values = self.main_map.get(key)
        if values is None:
            values = self.values_constructor()
            self.main_map.put(key, values)
        values.put(value, ...)

    def clear(self):
        self.main_map.clear()

    def __iter__(self) -> Iterator[Key]:
        yield from self.main_map

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.main_map})"

    def validate(self):
        self.main_map.validate()
        for key in self:
            values = self.main_map.get(key)
            assert values is not None, "Values must not be None"
            values.validate()


