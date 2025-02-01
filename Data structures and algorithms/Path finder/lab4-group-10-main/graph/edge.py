from dataclasses import dataclass
from typing import TypeVar, Generic

V = TypeVar('V')

# Dataclasses provide a lot of methods for free, such as __init__ and comparison:
# https://docs.python.org/3/library/dataclasses.html
# 'frozen' means that we cannot modify elements after creation:
@dataclass(frozen=True)
class Edge(Generic[V]):
    """
    A class for weighted directed edges.
    """
    start: V
    end: V
    weight: float = 1

    def reverse(self) -> 'Edge[V]':
        """Returns a new edge with the direction reversed."""
        return Edge(self.end, self.start, self.weight)

    # Different ways of formatting edges.

    def to_string(self, include_start: bool, include_end: bool, with_weight: bool|None = None):
        if with_weight is None:
            with_weight = (self.weight != 1)
        start_str = str(self.start) if include_start else ""
        end_str = str(self.end) if include_end else ""
        if with_weight:
            w = self.weight
            decimals = 0 if w == round(w, 0) else 1 if w == round(w, 1) else 2
            return f"{start_str} --[{w:.{decimals}f}]-> {end_str}"
        else:
            return f"{start_str} -> {end_str}"

    def __str__(self):
        return self.to_string(True, True)

