import sys
import random
from collections.abc import Iterator
from dataclasses import dataclass

from .edge import Edge
from .graph import Graph
from .point import Point, ORIGIN


SEPARATOR = '/'

# The characters '_', 'A', ..., 'Z', '0', ..., '9', 'a', ..., 'z'.
# A fixed SlidingPuzzle uses only an initial prefix of these characters.
ALL_TILE_NAMES = (
    "_" +
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
    "0123456789" +
    "abcdefghijklmnopqrstuvwxyz"
)

MOVES = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1)
]


@dataclass(frozen=True)
class SlidingPuzzleState:
    """
    A possible state of the N-puzzle.

    We represent the tiles as numbers from 0 to N * M.
    The empty tile is represented by 0.

    The array `positions` stores the position of each tile.

    Optional task: try out different representations of states:
     - coding the positions as indices (sending a point p to p.y * M + p.x)
     - using an array `tiles` that stores the tile at each point
     - combinations (more space usage, but better runtime?)
    """
    N: int
    M: int
    positions: tuple[Point, ...]

    @staticmethod
    def parse(s: str) -> 'SlidingPuzzleState':
        """
        Parse a state from its string representation.
        For example, a valid string representation for N = M = 3 is "/FDA/CEH/GB_/".
        """
        rows = s.strip(SEPARATOR).split(SEPARATOR)
        N = len(rows)
        M = len(rows[0])
        positions = [ORIGIN] * (N * M)
        for y, row in enumerate(rows):
            if len(row) != M:
                raise ValueError(f"Row {row} does not have {M} columns.")
            for x, tile_name in enumerate(row):
                i = ALL_TILE_NAMES.index(tile_name)
                if positions[i] != ORIGIN:
                    raise ValueError(f"Duplicate tiles: {tile_name}")
                positions[i] = Point(x, y)
        return SlidingPuzzleState(N, M, tuple(positions))

    def swap(self, i: int, j: int) -> 'SlidingPuzzleState':
        """Returns the state given by swapping the tiles `i` and `j`."""
        if i > j:
            i, j = j, i
        assert 0 <= i < j < len(self.positions)
        return SlidingPuzzleState(
            self.N, self.M,
            self.positions[:i] +
            (self.positions[j],) +
            self.positions[i+1:j] +
            (self.positions[i],) +
            self.positions[j+1:]
        )

    def shuffled(self) -> 'SlidingPuzzleState':
        """Returns a randomly shuffled state."""
        return SlidingPuzzleState(
            self.N, self.M,
            tuple(random.sample(self.positions, len(self.positions)))
        )

    def tiles(self) -> tuple[tuple[int, ...], ...]:
        """Returns the NxM-matrix of tiles of this state."""
        tiles = [[0] * self.M for _ in range(self.N)]
        for i, p in enumerate(self.positions):
            tiles[p.y][p.x] = i
        return tuple(tuple(t) for t in tiles)

    def __str__(self):
        return SEPARATOR + SEPARATOR.join(
            ''.join(ALL_TILE_NAMES[i] for i in tl)
            for tl in self.tiles()
        ) + SEPARATOR


class SlidingPuzzle(Graph[SlidingPuzzleState]):
    """
    A generalization of the 15-puzzle.

    The nodes are string encodings of an N x M matrix of tiles.
    The tiles are represented by characters starting from the letter A
    (for example, A...H for N=M=3, and A...O for N=M=4).
    The empty tile is represented by "_", and
    to make it more readable for humans every row is separated by "/".
    """
    N: int
    M: int

    def __init__(self, graph: str|tuple[int,int]|None = None):
        if graph:
            self.init(graph)

    def init(self, graph: str|tuple[int,int]):
        """Creates a new sliding puzzle of dimensions N x M."""
        if isinstance(graph, str):
            try:
                n, m = map(int, graph.split('x'))
            except (ValueError, TypeError):
                raise ValueError(f"Invalid dimensions (e.g., 3x3): {graph}")
        else:
            (n, m) = graph
        if not (n >= 1 and m >= 1): raise ValueError("The dimensions must be positive.")
        if m * n > 40: raise ValueError("We only support up to 40 tiles.")
        self.N, self.M = n, m  # type: ignore
        # (Reason for type:ignore: pylance complains that N and M are upper-case)

    def nodes(self) -> frozenset[SlidingPuzzleState]:
        """
        All states are nodes of this graph.
        However, the set of such nodes is typically too large to enumerate.
        So we do not implement those operations.
        """
        raise NotImplementedError("too expensive!")

    def outgoing_edges(self, v: SlidingPuzzleState) -> list[Edge[SlidingPuzzleState]]:
        empty_pos = v.positions[0]
        edges: list[Edge[SlidingPuzzleState]] = []
        for move in MOVES:
            p = empty_pos.subtract(move)
            if self.is_valid_point(p):
                i = v.positions.index(p)
                new_state = v.swap(0, i)
                edges.append(Edge(v, new_state))
        return edges

    def is_weighted(self) -> bool:
        return False

    def is_valid_point(self, p:Point) -> bool:
        """Checks if the point is valid (lies inside the matrix)."""
        return 0 <= p.x < self.M and 0 <= p.y < self.N

    def guess_cost(self, v: SlidingPuzzleState, w: SlidingPuzzleState) -> float:
        """
        We guess the minimal cost for getting from one puzzle state to another,
        as the sum of the Manhattan displacement for each tile.
        The Manhattan displacement is the Manhattan distance from where
        the tile is currently to its desired location.
        """
        cost = 0
        for i in range(1, self.N * self.M):
            displacement = v.positions[i].subtract(w.positions[i])
            cost += abs(displacement.x) + abs(displacement.y)
        return cost

    def goal_state(self) -> SlidingPuzzleState:
        """
        Return the traditional goal state.
        The empty tile is in the bottom right corner.
        """
        return SlidingPuzzleState(self.N, self.M, tuple([
            Point(self.N-1, self.M-1)
        ] + [
            Point(i % self.M, i // self.M)
            for i in range(self.N * self.M - 1)
        ]))

    def parse_node(self, s: str):
        return SlidingPuzzleState.parse(s)

    def random_nodes(self) -> Iterator[SlidingPuzzleState]:
        while True:
            yield self.goal_state().shuffled()

    def __str__(self) -> str:
        N = self.N
        M = self.M
        return (
            f"SlidingPuzzle graph of size {N} x {M}.\n\n" +
            f"States are {N} x {M} matrices of unique characters in " +
            f"'{ALL_TILE_NAMES[1]}'...'{ALL_TILE_NAMES[N*M-1]}',\n" +
            f"and '{ALL_TILE_NAMES[0]}' (for the empty tile); " +
            f"rows are interspersed with '{SEPARATOR}'.\n" +
            f"The traditional goal state is: {self.goal_state()}.\n" +
            "\nRandom example nodes with outgoing edges:\n" +
            self.example_outgoing_edges(8)
        )


if __name__ == '__main__':
    (_, size) = sys.argv
    puzzle = SlidingPuzzle(size)
    print(puzzle)

