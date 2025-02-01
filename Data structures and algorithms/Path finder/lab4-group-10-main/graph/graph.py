import random
from abc import ABC, abstractmethod
from typing import Generic
from collections.abc import Iterator

from .edge import Edge, V


class Graph(ABC, Generic[V]):
    """
    An interface for directed graphs.

    Note that this interface differs from the graph interface in the course API:
    - it lacks several of the methods in the course API,
    - it has an additional method `guess_cost`.
    """

    @abstractmethod
    def __init__(self, graph: str|None = None): ...

    @abstractmethod
    def init(self, graph: str):
        """Initialises a graph from a file or a name or other description."""

    @abstractmethod
    def nodes(self) -> frozenset[V]:
        """
        Returns an unmodifiable set of nodes of this graph.
        """

    @abstractmethod
    def outgoing_edges(self, v: V) -> list[Edge[V]]:
        """Returns a collection of the graph edges that originate from the given node."""

    @abstractmethod
    def is_weighted(self) -> bool:
        """Returns if the graph edges are weighted."""

    def guess_cost(self, v: V, w: V) -> float:
        """
        Returns the guessed best cost for getting from v to w.
        The default guessed cost is 0, which is always admissible.
        """
        return 0.0

    # Below are some auxiliary methods.
    # You don't have to look at them.
    # They are used for parsing and printing.

    def num_nodes(self) -> int:
        """Returns the number of nodes in this graph."""
        return len(self.nodes())

    def num_edges(self) -> int:
        """
        Returns the number of edges in this graph.
        (Warning: the default implementation is inefficient).
        """
        return sum(len(self.outgoing_edges(v)) for v in self.nodes())

    @abstractmethod
    def parse_node(self, s: str) -> V:
        """
        Returns a node parsed from the given string.

        This is really an operation associated with the node type V, not Graph,
        but there's no easy way to do that in Python.
        So the result is not related to the nodes currently contained in the graph.
        """

    def draw_graph(
            self,
            max_width: int,
            max_height: int,
            start: V | None,
            goal: V | None,
            solution: list[Edge[V]] | None,
    ) -> str | None:
        """
        Returns a graphical string representation of the graph.
        If provided, start and end nodes and a path are marked.

        Only implemented for grid graphs.
        """
        return None

    def random_nodes(self) -> Iterator[V]:
        """Generate an infinite stream of random nodes."""
        node_list = list(self.nodes())
        while True:
            yield random.choice(node_list)

    def example_outgoing_edges(self, limit: int) -> str:
        """A helper method for printing some graph information."""
        lines: list[str] = []
        for k, start in enumerate(self.random_nodes()):
            if k >= limit:
                break
            outgoing = self.outgoing_edges(start)
            if not outgoing:
                lines.append(f"* {start} with no outgoing edges")
            else:
                ends: list[str] = []
                for edge in outgoing:
                    if self.is_weighted():
                        w = edge.weight
                        decimals = 0 if w == round(w, 0) else 1 if w == round(w, 1) else 2
                        ends.append(f"{edge.end} [{w:.{decimals}f}]")
                    else:
                        ends.append(str(edge.end))
                lines.append(f"* {start} ---> " + ", ".join(ends))
        return "\n".join(lines)

