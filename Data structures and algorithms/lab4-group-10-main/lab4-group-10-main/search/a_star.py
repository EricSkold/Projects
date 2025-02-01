from dataclasses import dataclass
from functools import total_ordering

from .searcher import Result
from .dijkstra import Dijkstra, DijkstraEntry, V

from utilities.priority_queue import PriorityQueue


@total_ordering         # This means that we only have to define __lt__
@dataclass(frozen=True) # 'frozen' means that we cannot modify elements after creation
class AStarEntry(DijkstraEntry[V]):
    """
    Entries of the priority queue.
    This inherits all instance variables from `DijkstraEntry`, plus the ones you add.

    To create an instance: `AStarEntry(node, last_edge, back_pointer, cost_to_here, ...)`
    """
    # These are inherited from DijkstraEntry:
    # node: V
    # last_edge: Optional[Edge[V]]             # None for the starting entry
    # back_pointer: Optional['AStarEntry[V]']  # None for the starting entry
    # cost_to_here: float

    #---------- TASK 3: A* search, priority queue entries --------------------#
    estimated_total_cost: float

    def __lt__(self, other: 'DijkstraEntry[V]'):
        '''The entry `self` is strictly smaller than `other`.'''
        assert isinstance(other, AStarEntry)
        
        return self.estimated_total_cost < other.estimated_total_cost
    #---------- END TASK 3 ---------------------------------------------------#


class AStar(Dijkstra[V]):
    """
    The A* algorithm for finding the shortest path.
    """

    def search(self) -> Result[V]:
        """
        Runs the A* algorithm to find a path in `graph` from `start` to `goal`.
        Returns the search result (which includes the path found if successful).
        """
        iterations = 0
        pqueue: PriorityQueue[AStarEntry[V]] = PriorityQueue()

        #---------- TASK 3: A* search, the main search algorithm -----------------#
        # TODO: Replace these lines with your solution!
        # Notes:
        # * You can start from your implementation of Dijkstra (but using AStarEntry now).
        # * Increment `iterations` every time you remove an entry from the priority queue.

        visited = set()

        # Add the start node to the priority queue
        pqueue.add(AStarEntry(self.start, None, None, 0, self.graph.guess_cost(self.start, self.goal)))
        
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

                estimated_total_cost = cost_to_here + self.graph.guess_cost(neighbor, self.goal)
                pqueue.add(AStarEntry(neighbor, edge, entry, cost_to_here, estimated_total_cost))
            
        return self.failure(iterations)

        #---------- END TASK 3 ---------------------------------------------------#

