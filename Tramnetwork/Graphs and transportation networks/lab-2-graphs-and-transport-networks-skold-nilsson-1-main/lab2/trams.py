import json
import graphs as gr
import sys
sys.path.append("lab1")
import tramdata as td
TRAM_FILE = "lab1/tramnetwork.json"


class TramStop:
    def __init__(self, name, lines=[], lat=None, lon=None):
        self._lines = lines
        self._name = name
        self._position = (lat, lon)

    def add_line(self, line):
        self._lines.append(line)

    def get_lines(self):
        return sorted(self._lines)

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position = lat, lon


class TramLine:
    def __init__(self, num, stops):
        self._number = str(num)
        self._stops = stops

    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops


class Tramnetwork(gr.WeightedGraph):
    def __init__(self, lines, stops, times):
        super().__init__()
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times

    def all_lines(self):
        return set(self._linedict.keys())

    def all_stops(self):
        return set(self._stopdict.keys())

    def extreme_positions(self):
        l_lat = min(self._stopdict, key=lambda x: self._stopdict[x]["lat"])
        l_lon = min(self._stopdict, key=lambda x: self._stopdict[x]["lon"])
        h_lat = max(self._stopdict, key=lambda x: self._stopdict[x]["lat"])
        h_lon = max(self._stopdict, key=lambda x: self._stopdict[x]["lon"])
        return {"lat": {'min':l_lat, 'max':h_lat}, "lon": {'min':l_lon, 'max':h_lon}}

    def geo_distance(self, a, b):
        return td.distance_between_stops(self._stopdict, a, b)

    def line_stops(self, line):
        return self._linedict[line]

    def stop_lines(self, a):
        return td.lines_via_stop(a)

    def stop_position(self, a):
        return self._stopdict[a]

    def transition_time(self, a, b):
        if a in self._timedict and b in self._timedict[a]:
            return self._timedict[a][b]
        elif b in self._timedict and a in self._timedict[b]:
            return self._timedict[b][a]


def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, "r", encoding="utf-8") as data:
        tramnetwork = json.load(data)

        G = Tramnetwork(tramnetwork["lines"], tramnetwork["stops"], tramnetwork["times"])

        for key in G._timedict:
            for stops in G._timedict[key].keys():
                G.add_edge(key, stops)
                G.set_weight(key, stops, G.transition_time(key, stops))
        for vertex in G.vertices():
            G.set_vertex_value(vertex, G.stop_position(vertex))
        return G


def demo():
    G = readTramNetwork()
    print(G.extreme_positions())
    a, b = input("from,to ").split(",")
    gr.view_shortest(G, a, b)


if __name__ == "__main__":
    demo()
