from hypothesis import given, strategies as st
import networkx as nx
import random
import unittest
import graphs as gr


def data():
    ints = st.integers(min_value=1, max_value=20)
    tups = st.tuples(ints, ints).filter(lambda x: x[0] != x[1])
    edgs = st.lists(tups, min_size=1, unique_by=(lambda x: x[0], lambda x: x[1]))
    verts = st.sets(ints, max_size=100)
    return st.tuples(ints, edgs, verts)


@given(data())
# If a has b as its neighbour, then b has a as its neighbour
def test_neighbours(data):
    T = nx.Graph()
    T.add_edges_from(data[1])
    G = gr.WeightedGraph(start=data[1])
    for ed in data[1]:
        neigh = T.neighbors(int(ed[0]))
        neighb = G.neighbours(ed[0])
        x = str(ed[1])
        assert x in neighb
        assert int(x) in neigh


@given(data())
# If (a, b) is in edges(), both a and b are in vertices()
def test_edges(data):
    T = nx.Graph()
    T.add_edges_from(data[1])
    G = gr.WeightedGraph(start=data[1])
    for tup in G.edges():
        assert tup[0] in G.vertices() and tup[1] in G.vertices()
        assert int(tup[0]) in list(T.nodes()) and int(tup[1]) in list(T.nodes())


@given(data())
# Tests the edge removal methods of class Graph
def edge_vertex_removal(data):
    T = nx.Graph()
    T.add_edges_from(data[1])
    G = gr.WeightedGraph(start=data[1])
    G._weightlist = {ed: random.randint(1, 20) for ed in G.edges()}
    G._valuelist = {vert: random.randint(1, 20) for vert in G.vertices()}
    for edge in data[1]:
        G.remove_edge(edge)
        T.remove_edge(edge)
        assert edge not in G.edge_list and edge not in G._weightlist
        assert edge not in T.edges()
    for vertex in G.vertices():
        G.remove_vertex(vertex)
        T.remove_node(vertex)
        assert (
            vertex not in G.vertices()
            and vertex not in G._adjlist
            and vertex not in G._valuelist
        )
        assert vertex not in T.nodes()


@given(data())
# The shortest path from a to b is the reverse of the shortest path from b to a
# (but notice that this can fail in situations where there are several shortest paths)
def test_dijkstra(data):
    G = gr.WeightedGraph(start=data[1])
    for edge in G.edges():
        G.set_weight(*edge, random.randint(1, 20))
    vertices = G.vertices()

    for vertex in vertices:
        for other_vert in vertices[vertices.index(vertex) + 1 :]:
            path1 = gr.dijkstra(G, vertex, cost=G.get_weight)
            path2 = gr.dijkstra(G, other_vert, cost=G.get_weight)
            if other_vert in path1 and vertex in path2:
                p1 = path1[other_vert]["path"]
                p2 = path2[vertex]["path"]
                t1 = path1[other_vert]["cost"]
                t2 = path2[vertex]["cost"]
                p2.reverse()

                assert t1 == t2 and p1 == p2, f"{p1,p2,t1,t2}"


class TestNxGraph(unittest.TestCase):
    def setUp(self):
        self.graph_attributes = [
            "neighbours",
            "vertices",
            "edges",
            "__len__",
            "add_vertex",
            "add_edge",
            "remove_vertex",
            "remove_edge",
            "get_vertex_value",
            "set_vertex_value",
            "is_directed",
        ]
        self.gen_graph = nx.erdos_renyi_graph(100, 0.7)
        self.edges = list(self.gen_graph.edges())

    # Compares dijkstra between native implementation and networkx
    def test_Nx_dijkstra(self):
        graph = nx.Graph()
        G = gr.WeightedGraph(start=self.edges)
        for edge in self.edges:
            node1, node2 = edge
            w = random.randint(1, 20)
            graph.add_edge(node1, node2, weight=w)
            G.set_weight(*edge, w)

        for source in G.vertices():
            costs = dict(nx.all_pairs_dijkstra_path_length(graph))[int(source)]
            path1 = dict(nx.all_pairs_dijkstra_path(graph, weight="weight"))[
                int(source)
            ]
            path2 = gr.dijkstra(G, source, G.get_weight)
            for key in path1:
                if str(key) != source:
                    self.assertEqual(
                        costs[key], path2[str(key)]["cost"], msg="Cost is not equal!"
                    )
                    self.assertEqual(
                        list(map(str, path1[key])),
                        path2[str(key)]["path"],
                        msg=f"path: {path2}",
                    )

    # Tests that all attributes and methods required have been implemented
    def test_attrib(self):
        for attrib in self.graph_attributes:
            self.assertTrue(hasattr(gr.Graph, attrib))
            self.assertTrue(hasattr(gr.WeightedGraph, attrib))


if __name__ == "__main__":
    unittest.main()
    test_neighbours()
    test_edges()
    test_dijkstra()
