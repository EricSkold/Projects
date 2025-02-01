import sys

from .edge import Edge
from .graph import Graph


Node = str

class AdjacencyGraph(Graph[Node]):
    """
    This is a class for a generic finite graph, with string nodes.
     - The edges are stored as an adjacency list as described in the course book and the lectures.
     - The graphs can be anything, such as a road map or a web link graph.
     - The graph can be read from a simple text file with one edge per line.
    """
    adjacency_list: dict[Node, list[Edge[Node]]]
    weighted: bool

    def __init__(self, graph: str|None = None):
        self.adjacency_list = {}
        self.weighted = False
        if graph:
            self.init(graph)

    def init(self, graph: str):
        """
        Populates the graph with edges from a text file.
        The file should contain one edge per line, each on the form
        "from \\t to \\t weight" or "from \\t to" (where \\t == TAB).
        """
        if graph:
            with open(graph, encoding="utf-8") as IN:
                for line in IN:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        start, end, *maybe_weight = line.split('\t')
                        if (not maybe_weight):
                            self.add_edge(Edge(start, end))
                        else:
                            weight = float(maybe_weight[0])
                            self.add_edge(Edge(start, end, weight))

    def add_node(self, v: Node):
        """Adds a node to this graph."""
        self.adjacency_list.setdefault(v, [])

    def add_edge(self, e: Edge[Node]):
        """
        Adds a directed edge (and its source and target nodes) to this edge-weighted graph.
        Note: This does not test if the edge is already in the graph!
        """
        self.add_node(e.start)
        self.add_node(e.end)
        self.adjacency_list[e.start].append(e)
        if not self.weighted and e.weight != 1:
            self.weighted = True

    def nodes(self) -> frozenset[Node]:
        return frozenset(self.adjacency_list)

    def outgoing_edges(self, v: Node) -> list[Edge[Node]]:
        return self.adjacency_list.get(v, [])

    def is_weighted(self) -> bool:
        return self.weighted

    def parse_node(self, s: str):
        if s not in self.adjacency_list:
            raise ValueError(f"Unknown node: {s}")
        return s

    def __str__(self) -> str:
        return (
            ("Weighted" if self.weighted else "Unweighted") +
            f" adjacency graph with {self.num_nodes()} nodes and {self.num_edges()} edges.\n" +
            "\nRandom nodes with outgoing edges:\n" +
            self.example_outgoing_edges(8)
        )


if __name__ == '__main__':
    _, file = sys.argv
    graph = AdjacencyGraph(file)
    print(graph)

