import random

from graph.edge import Edge, V
from .searcher import Searcher, Result


class RandomWalk(Searcher[V]):
    """
    Perform a random walk in the graph, hoping to reach the goal.
    Warning: this class will give up if the random walk
    reaches a dead end or after 10,000 iterations.
    So a negative result does not mean there is no path.
    """

    def search(self) -> Result[V]:
        iterations = 0
        cost = 0.0
        path: list[Edge[V]] = []

        current = self.start
        while iterations < 10_000:
            iterations += 1
            if current == self.goal:
                return self.success(cost, path, iterations)

            neighbours = self.graph.outgoing_edges(current)
            if len(neighbours) == 0:
                break

            edge = random.choice(neighbours)
            path.append(edge)
            cost += edge.weight
            current = edge.end

        return self.failure(iterations)

