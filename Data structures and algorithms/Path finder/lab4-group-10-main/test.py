#!/usr/bin/env python3

# A file for testing your implementations.
# Change this code however you want.
#
# Pro-tip: write proper unit tests, e.g. by using the unittest library:
# https://docs.python.org/3/library/unittest.html


from graph.edge import Edge
from graph.adjacency_graph import AdjacencyGraph
from graph.sliding_puzzle import SlidingPuzzle
from graph.grid_graph import GridGraph
from graph.word_ladder import WordLadder

from search.random_walk import RandomWalk
from search.dijkstra import Dijkstra
from search.a_star import AStar

###############################################################################
## Test path finder algorithms.

def test():
    ## Create a new adjacency graph with the nodes a, b, c, d.

    graph = AdjacencyGraph()
    graph.add_edge(Edge("a", "b", 8))
    graph.add_edge(Edge("a", "c", 15))
    graph.add_edge(Edge("b", "c", 5))
    graph.add_edge(Edge("b", "d", 12))
    graph.add_edge(Edge("c", "d", 6))
    graph.add_edge(Edge("d", "a", 3))
    start = "a"
    goal = "d"
    # Exercise: draw the graph on a paper and run Dijkstra's algorithm by hand.

    ## When you're done with playing around with the simple graph:
    ## Uncomment to select which graph to test below.

    # graph_name = "graphs/AdjacencyGraph/citygraph-SE.txt"
    # start = "Stockholm"
    # goal = "Kiruna"
    # graph = AdjacencyGraph(graph_name)

    # start = "/_C/BA/"
    # goal = "/AB/C_/"
    # graph = SlidingPuzzle((2, 2))

    # graph_name = "graphs/GridGraph/maze-10x5.txt"
    # start = "1:1"
    # goal = "39:9"
    # graph = GridGraph(graph_name)

    # graph_name = "graphs/WordLadder/swedish-romaner.txt"
    # start = "eller"
    # goal = "glada"
    # graph = WordLadder(graph_name)

    # Now we select the search algorithm and run the search.
    searcher = RandomWalk(  # or Dijkstra or AStar
        graph, graph.parse_node(start), graph.parse_node(goal)
    )
    result = searcher.search()

    # Finally we show the result.
    show_full_path = False
    show_path_weights = True
    print(result.to_string(show_full_path, show_path_weights))
    # You can use this if you want to print the graph too (only for GridGraph):
    # print(result.to_string(show_full_path, show_path_weights, True, 100, 25))


if __name__ == "__main__":
    test()

