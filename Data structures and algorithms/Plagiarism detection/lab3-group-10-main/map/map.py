from abc import abstractmethod
from typing import TypeVar, Generic
from collections.abc import Iterable, Iterator, Sequence

###############################################################################
# Comparable types: only used for type checking.
# You don't have to understand this definition.

from abc import abstractmethod
from typing import Protocol, TypeVar

class ComparableProtocol(Protocol):
    """Protocol for annotating comparable types."""
    @abstractmethod
    def __lt__(self: 'Key', other: 'Key', /) -> bool: ...
    def __gt__(self: 'Key', other: 'Key', /) -> bool: ...
    def __le__(self: 'Key', other: 'Key', /) -> bool: ...
    def __ge__(self: 'Key', other: 'Key', /) -> bool: ...

Key = TypeVar('Key', bound=ComparableProtocol)
Value = TypeVar('Value')


###############################################################################
# Simple multimaps

class Map(Iterable[Key], Generic[Key, Value]):
    """
    An abstract class of simple maps (also known as dictionaries).
    """

    def is_empty(self) -> bool:
        """Returns true if the map contains no key-value mappings."""
        return self.size() == 0

    def contains_key(self, key: Key) -> bool:
        """Returns true if the map contains a mapping for the specified key."""
        return self.get(key) is not None

    def contains(self, key: Key, value: Value) -> bool:
        """Return true if the value is associated with the key."""
        if value is None:
            raise ValueError("Value is None")
        return self.get(key) == value

    def __len__(self) -> int:
        """Returns the number of keys."""
        return self.size()

    @abstractmethod
    def size(self) -> int:
        """Returns the number of keys."""

    @abstractmethod
    def get(self, key: Key) -> Value | None:
        """Get the value associated with a key, or None if it doesn't exist."""

    @abstractmethod
    def put(self, key: Key, value: Value):
        """Associates the specified value with the specified key."""

    @abstractmethod
    def clear(self):
        """Deletes all keys and values."""

    def __iter__(self) -> Iterator[Key]:
        return iter(self.keys())

    @abstractmethod
    def keys(self) -> Sequence[Key]:
        """Returns a tuple of all keys."""

    def show(self, max_level: int) -> str:
        """Show the contents of the map, down to a certain level."""
        return str(self)

    def __str__(self) -> str:
        classname = type(self).__name__
        if self.is_empty(): return f"{classname}(empty)"
        return f"{classname}(size {self.size()})"

    @abstractmethod
    def validate(self):
        """
        Validates that the map is correctly implemented according to the specification.
        Raises an AssertionError if there is anything wrong.
        """

