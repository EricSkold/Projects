import sys
import re
from math import sqrt

from .edge import Edge
from .graph import Graph
from .point import Point


class GridGraph(Graph[Point]):
    """
    GridGraph is a 2D-map encoded as a bitmap, or an N x M matrix of characters.

    Some characters are passable, others denote obstacles.
    A verte is a point in the bitmap, consisting of an x- and a y-coordinate.
    This is defined by the helper class `Point`.
    You can move from each point to the eight point around it.
    The edge costs are 1.0 (for up/down/left/right) and sqrt(2) (for diagonal movement).
    The graph can be read from a simple ASCII art text file.
    """
    grid: list[str]

    # Characters from Moving AI Lab:
    #   . - passable terrain
    #   G - passable terrain
    #   @ - out of bounds
    #   O - out of bounds
    #   T - trees (unpassable)
    #   S - swamp (passable from regular terrain)
    #   W - water (traversable, but not passable from terrain)
    # Characters from http://www.delorie.com/game-room/mazes/genmaze.cgi
    #   | - +  walls
    #   space  passable
    allowed_chars = ".G@OTSW +|-"
    passable_chars = ".G "

    # The eight directions, as points.
    directions = [
        Point(x, y)
        for x in [-1, 0, 1] for y in [-1, 0, 1]
        if not (x == y == 0)
    ]

    def width(self) -> int:
        return len(self.grid[0])

    def height(self) -> int:
        return len(self.grid)

    def __init__(self, graph: str|list[str]|None = None):
        if graph:
            self.init(graph)

    def init(self, graph: str|list[str]):
        """
        Initialises the graph with edges from a text file,
        or from a grid of characters.
        The file describes the graph as ASCII art,
        in the format of the graph files from the Moving AI Lab.
        """
        if isinstance(graph, str):
            with open(graph, encoding="utf-8") as IN:
                graph = [
                    line for line in IN.read().splitlines()
                    if re.match("^[" + GridGraph.allowed_chars + "]+$", line)
                ]
        self.grid = graph
        for row in self.grid:
            if len(row) != self.width():
                raise ValueError("Malformed grid, row widths doesn't match.")

    def passable(self, p: Point) -> bool:
        """Returns true if you're allowed to pass through the given point."""
        return (
            0 <= p.x < self.width() and
            0 <= p.y < self.height() and
            self.grid[p.y][p.x] in self.passable_chars
        )

    def nodes(self) -> frozenset[Point]:
        # Note: this is inefficient because it calculates the set each time.
        return frozenset(
            p for y in range(self.height())
            for x in range(self.width())
            if self.passable(p := Point(x, y))
        )

    def outgoing_edges(self, v: Point) -> list[Edge[Point]]:
        return [
            edge
            # We consider all directions...
            for dir in self.directions
            # ...compute the edge in that direction...
            for edge in [Edge(v, v.add(dir), sqrt(dir.x*dir.x + dir.y*dir.y))]
            # ...and keep the ones with passable target.
            if self.passable(edge.end)
        ]

    def is_weighted(self) -> bool:
        return True

    def guess_cost(self, v: Point, w: Point) -> float:
        """
        Returns the guessed best cost for getting from one point to another.
        (the Euclidean distance between the points)
        """
        #---------- TASK 4: Guessing the cost, GridGraph ---------------------#
        dx = w.x - v.x
        dy = w.y - v.y
        return sqrt(dx ** 2 + dy ** 2)
        #---------- END TASK 4 -----------------------------------------------#

    def parse_node(self, s: str) -> Point:
        """
        Parse a point from a string representation.
        For example, a valid string representation is "39:18".
        """
        return Point.parse(s)

    def draw_graph(
            self,
            max_width: int,
            max_height: int,
            start: Point | None = None,
            goal: Point | None = None,
            solution: list[Edge[Point]] | None = None,
    ) -> str:
        path_points: set[Point] = set()
        if solution:
            for e in solution:
                path_points.add(e.start)
                path_points.add(e.end)

        lines: list[str] = []
        for y, row in enumerate(self.grid):
            if y >= max_height:
                lines.append("(truncated)")
                break
            line: list[str] = []
            for x, p in enumerate(row):
                if y == 0 and x >= max_width - 10:
                    line.append(" (truncated)")
                    break
                if x >= max_width:
                    break
                point = Point(x, y)
                line.append(
                    'S' if point == start else
                    'G' if point == goal else
                    '*' if point in path_points else p
                )
            lines.append("".join(line))
        return "\n".join(lines)

    def __str__(self) -> str:
        """
        Returns a string representation of this graph, including some random points and edges.
        """
        return (
            f"Grid graph of dimensions {self.width()} x {self.height()}.\n\n" +
            self.draw_graph(100, 25) +
            "\n\nRandom example nodes with outgoing edges:\n" +
            self.example_outgoing_edges(8)
        )


if __name__ == '__main__':
    (_, file) = sys.argv
    graph = GridGraph(file)
    print(graph)

