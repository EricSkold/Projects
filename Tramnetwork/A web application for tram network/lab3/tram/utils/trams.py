import json
import ast

# imports added in Lab3 version
import math
import os
from .graphs import WeightedGraph, dijkstra
from django.conf import settings


# # path changed from Lab2 version
# TODO: copy your json file from Lab 1 here
TRAM_FILE = os.path.join(settings.BASE_DIR, "static/tramnetwork.json")


# TODO: use your lab 2 class definition, but add one method
class TramNetwork(WeightedGraph):
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

        l_lat = self._stopdict[min(self._stopdict, key=lambda x: self._stopdict[x]["lat"])]["lat"]
        l_lon = self._stopdict[min(self._stopdict, key=lambda x: self._stopdict[x]["lon"])]["lon"]
        h_lat = self._stopdict[max(self._stopdict, key=lambda x: self._stopdict[x]["lat"])]["lat"]
        h_lon = self._stopdict[max(self._stopdict, key=lambda x: self._stopdict[x]["lon"])]["lon"]
        
        return l_lat, l_lon, h_lat, h_lon

    def distance_between_stops(stopdict, stop1, stop2):

        mean_latitude = math.radians((stopdict[stop1]["lat"] + stopdict[stop2]["lat"]) / 2)
        delta_latitude = math.radians(stopdict[stop1]["lat"] - stopdict[stop2]["lat"])
        delta_longitude = math.radians(stopdict[stop1]["lon"] - stopdict[stop2]["lon"])
        radius = 6371.009

        return round(
            radius
            * math.sqrt((delta_latitude**2) + (math.cos(mean_latitude) * delta_longitude) ** 2),3,)

    def geo_distance(self, a, b):
        return TramNetwork.distance_between_stops(self._stopdict, a, b)

    def line_stops(self, line):
        return self._linedict[line]

    def stop_lines(self, a):
        return [line for line in self._linedict if a in self._linedict[line]]

    def stop_position(self, a):
        return self._stopdict[a].get("lat"), self._stopdict[a].get("lon")

    def transition_time(self, a, b):
        if a in self._timedict and b in self._timedict[a]:
            return self._timedict[a][b]
        elif b in self._timedict and a in self._timedict[b]:
            return self._timedict[b][a]


def readTramNetwork(tramfile=TRAM_FILE):
    
    with open(tramfile, "r", encoding="utf-8") as data:
        tramnetwork = json.load(data)

        G = TramNetwork(tramnetwork["lines"], tramnetwork["stops"], tramnetwork["times"])

        for key in G._timedict:
            for stops in G._timedict[key].keys():
                G.add_edge(key, stops)
                G.set_weight(key, stops, G.transition_time(key, stops))

        for vertex in G.vertices():
            G.set_vertex_value(vertex, G.stop_position(vertex))
        return G


# Bonus task 1: take changes into account and show used tram lines


def specialize_stops_to_lines(network):

    vertices = {(stop, line) for stop in network.vertices() for line in network.stop_lines(stop)}

    new_edges = {
        ((stop1, line), (stop2, line))
        for stop1, stop2 in network.edges()
        for line in network._linedict
        if stop1 in network._linedict[line] and stop2 in network._linedict[line]
    }

    same_stop_edges = set()
    for vertex in vertices:
        same_stops = {v for v in vertices if v[0] == vertex[0] and v[1] != vertex[1]}
        for stop in same_stops:
            if (stop, vertex) not in same_stop_edges:
                same_stop_edges.add((vertex, stop))

    network._adjlist.clear()
    network._valuelist.clear()
    network.edge_list.clear()
    network._weightlist.clear()

    all_edges = new_edges.union(same_stop_edges)

    for vertex in vertices:
        network.add_vertex(vertex)
        network.set_vertex_value(vertex, network.stop_position(vertex[0]))

    for edge in all_edges:
        network.add_edge(*edge)

    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    a = ast.literal_eval(a)
    b = ast.literal_eval(b)
    if a[0] != b[0]:
        changetime = spec_network.transition_time(a[0], b[0])
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    a = ast.literal_eval(a)
    b = ast.literal_eval(b)
    if a[0] != b[0]:
        changedistance = spec_network.geo_distance(a[0], b[0])
    return changedistance
