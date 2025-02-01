#!/usr/bin/env python3

"""
This is the main file for finding paths in graphs.
Depending on the command line arguments,
it creates different graphs and runs different search algorithms.
"""

import sys
from typing import Any

from graph.graph import Graph, V
from graph.adjacency_graph import AdjacencyGraph
from graph.sliding_puzzle import SlidingPuzzle
from graph.grid_graph import GridGraph
from graph.word_ladder import WordLadder

from search.searcher import Searcher
from search.random_walk import RandomWalk
from search.dijkstra import Dijkstra
from search.a_star import AStar

from utilities.command_parser import CommandParser
from utilities.stopwatch import Stopwatch


# Settings for showing the solution - you can change these if you want.
show_full_path = False
show_path_weights = True
show_grid_graph = True
max_grid_graph_width = 100
max_grid_graph_height = 25


searchers: dict[str, type[Searcher[Any]]] = {
    "Random": RandomWalk,
    "Dijkstra": Dijkstra,
    "AStar": AStar,
}

graph_types: dict[str, type[Graph[Any]]] = {
    "AdjacencyGraph": AdjacencyGraph,
    "GridGraph": GridGraph,
    "SlidingPuzzle": SlidingPuzzle,
    "WordLadder": WordLadder,
}

parser = CommandParser(description=(__doc__ or "").strip())
parser.add_argument("--algorithm", "-a", required=True, choices=searchers.keys(),
                    help="search algorithm to test")
parser.add_argument("--graphtype", "-t", required=True, choices=graph_types.keys(),
                    help="type of graph")
parser.add_argument("--graph", "-g", required=True,
                    help="the graph itself")
parser.add_argument("--queries", "-q", nargs="*",
                    help="list of alternating start and goal nodes")


def main():
    options = parser.parse_args()

    GraphType = graph_types[options.graphtype]
    graph: Graph[Any]
    graph = GraphType(options.graph)

    algorithm: type[Searcher[Any]]
    algorithm = searchers[options.algorithm]

    if not options.queries:
        search_interactive(algorithm, graph)
    else:
        if len(options.queries) % 2 != 0:
            raise ValueError("There must be an even number of query nodes")
        for i in range(0, len(options.queries), 2):
            start = options.queries[i]
            goal = options.queries[i+1]
            search_once(algorithm, graph, start, goal)


def search_interactive(algorithm: type[Searcher[V]], graph: Graph[V]):
    print(graph)
    print()
    while True:
        try:
            start = input("Start: ")
        except EOFError:
            print()
            break
        if not start.strip():
            break
        goal = input("Goal: ")
        print()
        search_once(algorithm, graph, start, goal)
    print("Bye bye, hope to see you again soon!")


def search_once(algorithm: type[Searcher[V]], graph: Graph[V], start: str, goal: str):
    try:
        start_node = graph.parse_node(start.strip())
        goal_node = graph.parse_node(goal.strip())
    except ValueError as e:
        print("Parse error!", file=sys.stderr)
        print(e, file=sys.stderr)
        print(file=sys.stderr)
        return

    print(f"Searching for a path from {start_node} to {goal_node}...")
    stopwatch = Stopwatch()
    result = algorithm(graph, start_node, goal_node).search()
    stopwatch.finished("Searching the graph")
    print(result.to_string(show_full_path, show_path_weights, show_grid_graph, max_grid_graph_width, max_grid_graph_height))
    print()


if __name__ == '__main__':
    main()

