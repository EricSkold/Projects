# TODO: mock-up to be replaced by your file from Lab 2

class Graph:
    def __init__(self, start=None, values=None, directed=False):
        self._adjlist = {}
        if values is None:
            values = {}
        if start is None:
            start = []

        self._valuelist = values
        self.edge_list = [self._tupconvert(a, b) for a, b in start if start]
        self._isdirected = directed

        for edge in self.edge_list:
            self.add_edge(*edge)

    def __len__(self):
        return len(self.vertices())

    def _tupconvert(self, a, b):
        return tuple(sorted((str(a), str(b))))

    def vertices(self):
        return list(self._adjlist.keys())

    def edges(self):
        self.edge_list.sort(key=lambda x: (x[0], x[1]))
        return self.edge_list

    def neighbours(self, v):
        return self._adjlist.get(str(v), {})

    def add_edge(self, a, b):
        vertice_tup = self._tupconvert(a, b)
        for index, vertice in enumerate(vertice_tup):
            other_vertice = vertice_tup[abs(index - 1)]
            if vertice in self._adjlist:
                if other_vertice not in self._adjlist[vertice]:
                    self._adjlist[vertice].append(other_vertice)
            else:
                self._adjlist[vertice] = [other_vertice]
        if vertice_tup not in self.edge_list:
            self.edge_list.append(vertice_tup)

    def add_vertex(self, a):
        if str(a) not in self._adjlist:
            self._adjlist[str(a)] = []

    def remove_vertex(self, vertex):
        vertex = str(vertex)
        if vertex in self._adjlist:
            self._adjlist.pop(vertex)
            for ed in self._adjlist:
                if vertex in self.neighbours(ed):
                    self._adjlist[ed].remove(vertex)
        self.edge_list = [edge for edge in self.edge_list if vertex not in edge]
        self._valuelist.pop(vertex)

    def remove_edge(self, a, b):
        edge_tup = self._tupconvert(a, b)
        if edge_tup in self.edge_list:
            self.edge_list.remove(edge_tup)
        for key in list(self._adjlist):
            if key in [a, b]:
                self._adjlist.pop(key)
            for val in self.neighbours(key):
                if val in [a, b]:
                    self._adjlist[key].remove(val)

    def is_directed(self):
        return self.is_directed

    def get_vertex_value(self, v):
        return self._valuelist.get(str(v))

    def set_vertex_value(self, v, x):
        self._valuelist[str(v)] = x


class WeightedGraph(Graph):
    def __init__(self, start=None, values=None, directed=False):
        super().__init__(start, values, directed)
        self._weightlist = {}

    def set_weight(self, a, b, w):
        edges = self.edges()
        edge_tup = self._tupconvert(a, b)
        if edge_tup in edges:
            self._weightlist[edge_tup] = w

    def get_weight(self, a, b):
        return self._weightlist.get(self._tupconvert(a, b))

    def remove_edge(self, a, b):
        edge_tup = self._tupconvert(a, b)
        super().remove_edge(a, b)
        for edge in list(self._weightlist):
            if edge == edge_tup:
                self._weightlist.pop(edge)

    def remove_vertex(self, vertex):
        super().remove_vertex(vertex)
        for edge in list(self._weightlist):
            if vertex in edge:
                self._weightlist.pop(edge)


def dijkstra(graph, source, cost=lambda u, v: 1):
    q = set()
    dist = {}
    source = str(source)
    for vertex in graph.vertices():
        dist[vertex] = {"cost": float("inf"), "path": []}
        q.add(vertex)

    dist[source] = {"cost": 0, "path": []}

    while len(q) != 0:
        current_min_dist = min([item for item in dist.items() if item[0] in q], key=lambda x: x[1]["cost"])[0]

        q.remove(current_min_dist)

        for neighbour in graph.neighbours(current_min_dist):
            if neighbour in q:

                sorted_key = graph._tupconvert(current_min_dist, neighbour)
                alt_dist = dist[current_min_dist]["cost"] + cost(*sorted_key)

                if alt_dist < dist[neighbour]["cost"]:
                    dist[neighbour]["cost"] = alt_dist
                    dist[neighbour]["path"] = dist[current_min_dist]["path"] + [current_min_dist]

    dist.pop(source)
    for vertex in dist:
        if len(dist[vertex]["path"]) > 0:
            dist[vertex]["path"].append(vertex)
    return dist
