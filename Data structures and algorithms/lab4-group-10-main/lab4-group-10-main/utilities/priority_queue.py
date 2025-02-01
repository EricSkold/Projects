
import heapq
from typing import TypeVar, Generic, List

E = TypeVar('E')

class PriorityQueue(Generic[E]):
    """
    A class for priority queues, using Python's standard `heapq` module.
    Elements are ordered by their natural ordering, and the least elements
    is the one that is first in the queue.
    """
    heap: List[E]

    def __init__(self):
        self.heap = []

    def is_empty(self) -> bool:
        """Returns true if the priority queue is empty."""
        return len(self.heap) == 0

    def size(self) -> int:
        """Returns the number of elements in this priority queue."""
        return len(self.heap)

    def __len__(self) -> int:
        return self.size()

    def add(self, e: E):
        """Adds e to the priority queue."""
        heapq.heappush(self.heap, e)

    def remove_min(self) -> E:
        """
        Removes and returns the minimum element.
        Raises an IndexError if the priority queue is empty.
        """
        return heapq.heappop(self.heap)

    def get_min(self) -> E:
        """
        Returns the minimum element, without removing it.
        Raises an IndexError if the priority queue is empty.
        """
        return self.heap[0]


