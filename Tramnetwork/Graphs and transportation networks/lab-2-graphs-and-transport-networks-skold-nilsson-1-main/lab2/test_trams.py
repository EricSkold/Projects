import unittest
import trams as tr
import graphs as gr
import tramdata
import networkx as nx
import random

LINE_FILE = "lab1/data/tramlines.txt"


class TestTrams(unittest.TestCase):
    def setUp(self):
        self.graph = tr.readTramNetwork()
        self.edges = self.graph.edges()
        self.linedict = self.graph._linedict
        self.stopdict = self.graph._stopdict
        self.timedict = self.graph._timedict
        self.stopset = {stop for line in self.linedict for stop in self.linedict[line]}
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
            "all_lines",
            "all_stops",
            "extreme_positions",
            "geo_distance",
            "line_stops",
            "stop_lines",
            "stop_position",
            "transition_time",
        ]

    # test connectedness of tram network
    def test_dfs(self):
        graph = self.graph
        vertices = set(graph.vertices())
        stack = []
        start_node = random.choice(list(self.stopdict.keys()))
        stack.append(start_node)
        discovered_vertices = set()
        while stack:
            v = stack.pop()
            if v not in discovered_vertices:
                discovered_vertices.add(v)
                for neighbour in graph.neighbours(v):
                    stack.append(neighbour)
        self.assertEqual(vertices, discovered_vertices, msg="Graph not connected!")

    def test_stops_exist(self):
        for stop in self.stopset:
            self.assertIn(stop, self.stopdict, msg=stop + " not in stopdict")

    # Tests that all tram lines listed in the original text file tramlines.txt are included in linedict
    def test_lines(self):
        lines_native = [
            tramdata.retrieve_data(LINE_FILE)[0][item]
            for item in tramdata.retrieve_data(LINE_FILE)[1]
        ]
        lines_dict = list(self.linedict.keys())
        self.assertEqual(lines_native, lines_dict)

    # Tests that list of stops for each tramline is the same in tramlines.txt and linedict
    def test_stops(self):
        source_data = [item[0] for item in tramdata.retrieve_data(LINE_FILE)[0]]
        lines_index = tramdata.retrieve_data(LINE_FILE)[1]
        n = 0
        for line in self.linedict:
            if n + 1 < len(lines_index):
                self.assertEqual(
                    self.linedict[line],
                    source_data[lines_index[n] + 1 : lines_index[n + 1]],
                )
                n += 1

    # Tests that all distances less than 20 km
    def test_distances(self):
        checked_stops = set()
        for line in self.linedict:
            for stop in self.linedict[line]:
                for other_stops in self.linedict[line][
                    self.linedict[line].index(stop) + 1 :
                ]:
                    if (stop, other_stops) not in checked_stops:
                        self.assertLess(
                            self.graph.geo_distance(stop, other_stops),
                            20,
                        )
                        checked_stops.add((stop, other_stops))
                        checked_stops.add((other_stops, stop))

    # Tests that time from a to b is equal to time from b to a
    def test_timeCorrespondense(self):
        checked_stops = set()
        for line in self.linedict:
            for stop in self.linedict[line]:
                for other_stops in self.linedict[line][
                    self.linedict[line].index(stop) + 1 :
                ]:
                    if (stop, other_stops) not in checked_stops:
                        self.assertEqual(
                            self.graph.transition_time(stop, other_stops),
                            self.graph.transition_time(other_stops, stop),
                        )
                        checked_stops.add((stop, other_stops))
                        checked_stops.add((other_stops, stop))

    # Verifies that there's no redundancy in timesdict
    def test_duplicates(self):
        for stop in self.timedict:
            for sub_stop in list(self.timedict[stop].keys()):
                if sub_stop in self.timedict:
                    self.assertNotIn(stop, list(self.timedict[sub_stop].keys()))

    # Tests that timesdict contains all stops
    def test_times_exist(self):
        set1 = set()
        for stop in self.timedict:
            set1.add(stop)
            for element in list(self.timedict[stop].keys()):
                set1.add(element)

        self.assertEqual(set1, self.stopset)

    # Tests that timesdict include all possible transition pairs
    def test_time_combinations_exist(self):
        set1 = set()
        set2 = set()
        for line in self.linedict:
            for stop in self.linedict[line]:
                if self.linedict[line].index(stop) != len(self.linedict[line]) - 1:
                    set1.add(
                        (stop, self.linedict[line][self.linedict[line].index(stop) + 1])
                    )
                    set1.add(
                        (self.linedict[line][self.linedict[line].index(stop) + 1], stop)
                    )

        for time in self.timedict:
            for key in list(self.timedict[time].keys()):
                set2.add((time, key))
                set2.add((key, time))

        self.assertEqual(set1, set2)

    def test_attrib(self):
        for attrib in self.graph_attributes:
            self.assertTrue(hasattr(tr.Tramnetwork, attrib))

    # If a has b as its neighbour, then b has a as its neighbour
    def test_neighbours(self):
        T = nx.Graph()
        T.add_edges_from(self.edges)

        for ed in self.edges:
            nx_neigh = T.neighbors(ed[0])
            tr_neigh = self.graph.neighbours(ed[0])
            x = ed[1]
            assert x in tr_neigh
            assert x in nx_neigh

    # If (a, b) is in edges(), both a and b are in vertices()
    def test_edges(self):
        T = nx.Graph()
        T.add_edges_from(self.edges)
        for tup in self.edges:
            assert tup[0] in self.graph.vertices() and tup[1] in self.graph.vertices()
            assert tup[0] in list(T.nodes()) and tup[1] in list(T.nodes())

    def edge_vertex_removal(self):
        T = nx.Graph()
        T.add_edges_from(self.edges)
        self.graph._weightlist = {
            ed: random.randint(1, 20) for ed in self.graph.edges()
        }
        self.graph._valuelist = {
            vert: random.randint(1, 20) for vert in self.graph.vertices()
        }
        for edge in self.edges:
            self.graph.remove_edge(edge)
            T.remove_edge(edge)
            assert edge not in self.graph.edges() and edge not in self.graph._weightlist
            assert edge not in T.edges()
        for vertex in self.graph.vertices():
            self.graph.remove_vertex(vertex)
            T.remove_node(vertex)
            assert (
                vertex not in self.graph.vertices()
                and vertex not in self.graph._adjlist
                and vertex not in self.graph._valuelist
            )
            assert vertex not in T.nodes()

    # The shortest path from a to b is the reverse of the shortest path from b to a
    # (but notice that this can fail in situations where there are several shortest paths)
    def test_dijkstra(self):
        vertices = self.graph.vertices()

        for vertex in vertices:
            for other_vert in vertices[vertices.index(vertex) + 1 :]:
                path1 = gr.dijkstra(self.graph, vertex, cost=self.graph.get_weight)
                path2 = gr.dijkstra(self.graph, other_vert, cost=self.graph.get_weight)
                if other_vert in path1 and vertex in path2:
                    p1 = path1[other_vert]["path"]
                    p2 = path2[vertex]["path"]
                    t1 = path1[other_vert]["cost"]
                    t2 = path2[vertex]["cost"]
                    p2.reverse()

                    assert t1 == t2 and p1 == p2, f"{p1,p2,t1,t2}"


if __name__ == "__main__":
    unittest.main()
