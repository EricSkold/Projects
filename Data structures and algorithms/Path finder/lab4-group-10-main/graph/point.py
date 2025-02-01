
from typing import NamedTuple

# A named tuple is a tuple where each component has a name,
# we get all tuple methods for free.
class Point(NamedTuple):
    """
    A class for two-dimensional points with integral coordinates.
    Used in GridGraph and SlidingPuzzle.
    """
    x: int
    y: int

    def add(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def subtract(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"{self.x}:{self.y}"

    @staticmethod
    def parse(s: str) -> 'Point':
        try:
            return Point(*map(int, s.split(':')))
        except (ValueError, TypeError):
            raise ValueError(f"Not a legal representation of a Point: '{s}'")


ORIGIN = Point(0, 0)


