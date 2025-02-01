from typing import Generic
from dataclasses import dataclass
from functools import total_ordering

from graph.edge import Edge, V
from .searcher import Searcher, Result
from utilities.priority_queue import PriorityQueue


@total_ordering         # This means that we only have to define __lt__
@dataclass(frozen=True) # 'frozen' means that we cannot modify elements after creation
class DijkstraEntry(Generic[V]):
    """
    Entries of the priority queue.
    To create an instance: `DijkstraEntry(node, last_edge, back_pointer, cost_to_here)`
    """
    node: V
    last_edge: Edge[V] | None                # None for the starting entry
    back_pointer: 'DijkstraEntry[V] | None'  # None for the starting entry
    cost_to_here: float

    def __lt__(self, other: 'DijkstraEntry[V]') -> bool:
        """The entry `self` is strictly smaller than `other`."""
        return self.cost_to_here < other.cost_to_here


class Dijkstra(Searcher[V]):
    """
    Dijkstra's algorithm (uniform-cost search) for finding the shortest path.
    """

    def search(self) -> Result[V]:
        """
        Uniform cost search for a path in `graph` from `start` to `goal`.
        Returns the search result (which includes the path found if successful).
        """
        iterations = 0
        pqueue: PriorityQueue[DijkstraEntry[V]] = PriorityQueue()

        #---------- TASK 1a+c: Dijkstra's algorithm ------------------------------#
        # TODO: Replace these lines with your solution!
        # Notes:
        # * Use `self.graph`, `self.start`, `self.goal`.
        # * Increment `iterations` every time you remove an entry from the priority queue.
        # * Return one of the following search results:
        #   - `self.success(cost, path, iterations)`,
        #   - `self.failure(iterations)` if no path found.
        #   See the parent class Search for these methods.
        
        visited = set()

        # Add the start node to the priority queue
        pqueue.add(DijkstraEntry(self.start, None, None, 0))
        
        # While the priority queue is not empty
        while not pqueue.is_empty():
            entry = pqueue.remove_min()

            iterations += 1

            # If the node has already been visited, skip it
            if entry.node in visited:
                continue

            # Mark the node as visited
            visited.add(entry.node)

            # If the goal node is reached, return the path
            if entry.node == self.goal:
                return self.success(entry.cost_to_here, self.extract_path(entry), iterations)
            
            # Add the outgoing edges to the priority queue
            for edge in self.graph.outgoing_edges(entry.node):
                neighbor = edge.end
                cost_to_here = entry.cost_to_here + edge.weight

                pqueue.add(DijkstraEntry(neighbor, edge, entry, cost_to_here))
    
        return self.failure(iterations)

        #---------- END TASK 1a+c ------------------------------------------------#

    def extract_path(self, entry: 'DijkstraEntry[V]') -> list[Edge[V]]:
        """
        Extracts the path from the start to the current priority queue entry.
        """
        #---------- TASK 1b: Extracting the path ---------------------------------#        
        path = []
        while entry.last_edge is not None:
            path.append(entry.last_edge)
            entry = entry.back_pointer
        # Reverse the list to get the correct order
        path.reverse()
        return path
        #---------- END TASK 1b --------------------------------------------------#

