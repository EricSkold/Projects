from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic

from graph.edge import Edge
from graph.graph import Graph, V


class Searcher(ABC, Generic[V]):
    """
    This is an abstract class for a search query in a given graph.
    The graph as well as start and goal nodes are instance variables.
    Call `search` to perform a search and obtain the search result.
    """
    graph: Graph[V]
    start: V
    goal: V

    def __init__(self, graph: Graph[V], start: V, goal: V):
        self.graph = graph
        self.start = start
        self.goal = goal

    @abstractmethod
    def search(self) -> "Result[V]":
        """
        Searches for a path in `self.graph` from `self.start` to `self.goal`.
        Returns the search result (which includes the path found if successful).
        """

    def success(self, cost: float, path: list[Edge[V]]|None, iterations: int) -> "Result[V]":
        """Construct a success result (path found)."""
        return Result(self, True, cost, path, iterations)

    def failure(self, iterations: int) -> "Result[V]":
        """Construct a failure result (no path found)."""
        return Result(self, False, -1, None, iterations)


# Dataclasses provide a lot of methods for free, such as __init__ and comparison:
# https://docs.python.org/3/library/dataclasses.html
# 'frozen' means that we cannot modify elements after creation:
@dataclass(frozen=True)
class Result(Generic[V]):
    """
    A class for search results.
    You don't have to look into this.
    """
    query: Searcher[V]
    success: bool
    cost: float
    path: list[Edge[V]] | None
    iterations: int

    @property
    def graph(self):
        return self.query.graph

    @property
    def start(self):
        return self.query.start

    @property
    def goal(self):
        return self.query.goal

    def format_path_part(self, suffix: bool, with_weight: bool, i: int, j: int) -> str:
        assert self.path, "The path must not be None"
        return "".join(
            e.to_string(not suffix, suffix, with_weight and self.graph.is_weighted())
            for e in self.path[i:j]
        )

    def validate_path(self):
        if self.success:
            if self.path is None:
                raise ValueError("The path is null. Remember to implement extractPath.")
            if not isinstance(self.path, list):  # type: ignore
                raise ValueError("The path must be a list - did you forget to implement extract_path?")
            actual_cost = 0.0
            for e in self.path:
                actual_cost += e.weight
            if (self.cost != actual_cost):
                raise ValueError(f"The reported path cost {self.cost}"
                                 f" differs from the calculated cost {actual_cost}.")
        else:
            if self.path is not None:
                raise ValueError("Failure reported, but path is not null.")

    def validate_iterations(self):
        if self.iterations <= 0:
            raise ValueError("The number of iterations should be > 0.")

    def validate(self):
        self.validate_iterations()
        self.validate_path()

    def to_string(
            self,
            show_full_path: bool,
            with_weight: bool,
            draw_graph: bool = False,
            max_graph_width: int = 50,
            max_graph_height: int = 20,
    ) -> str:
        lines: list[str] = []
        try:
            self.validate_iterations()
            lines.append(f"Loop iteration count: {self.iterations}")
        except ValueError as e:
            lines.append(f"WARNING: {e}")

        if self.success:
            c = self.cost
            decimals = 0 if c == round(c, 0) else 1 if c == round(c, 1) else 2
            lines.append(f"Cost of path from {self.start} to {self.goal}: {c:.{decimals}f}")
        else:
            lines.append(f"No path from {self.start} to {self.goal} found.")

        try:
            self.validate_path()
        except ValueError as e:
            lines.append(f"WARNING: {e}")

        if isinstance(self.path, list):
            pathlen = len(self.path)
            lines.append(f"Number of edges: {pathlen}")
            if show_full_path or pathlen <= 10:
                lines.append(
                    str(self.path[0].start) +
                    self.format_path_part(True, with_weight, 0, pathlen)
                )
            else:
                lines.append(
                    self.format_path_part(False, with_weight, 0, 5) + "....." +
                    self.format_path_part(True, with_weight, pathlen-5, pathlen)
                )
            if draw_graph:
                graph_str = self.graph.draw_graph(
                        max_graph_width, max_graph_height, self.start, self.goal, self.path)
                if graph_str:
                    lines.append("")
                    lines.append(graph_str)

        return '\n'.join(lines)

