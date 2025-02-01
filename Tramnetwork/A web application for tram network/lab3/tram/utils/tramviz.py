# visualization of shortest path in Lab 3, modified to work with Django

from .trams import (
    specialize_stops_to_lines,
    specialized_transition_time,
    specialized_geo_distance,
    readTramNetwork,
)


from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import ast
from django.conf import settings


def show_shortest(dep, dest):

    network = specialize_stops_to_lines(readTramNetwork())

    def dijkstra_path(spec_network, a, b , cost_function = lambda u,v: 1):
        visited_paths = []
        for line in spec_network.stop_lines(a):
                
                path = dijkstra(spec_network, f"('{a}', '{line}')", cost=cost_function)
                min_path = min([path[key] for key in path if f"'{b}'" in key], key= lambda x: x['cost'])
                visited_paths.append(min_path)

        shortest_path = min(visited_paths, key=lambda x: x['cost'])
        shortest_path['path'] = list(map(ast.literal_eval, shortest_path['path']))
        return shortest_path

    
    def path_formatter(path):
        visited_stops = []
        lines = []
        formatted_path = []
        for stop in path:
            if stop[1] in lines and stop[0]:
                formatted_path.append(stop[0])
                visited_stops.append(stop[0])

            else:
                formatted_path.append(stop[1] + " " + stop[0])
                lines.append(stop[1])
                visited_stops.append(stop[0])
                

        return formatted_path,visited_stops

    quickest = dijkstra_path(network,dep,dest, cost_function=lambda u,v: specialized_transition_time(network,u,v))
    formatted_quick_path = path_formatter(quickest['path'])[0]
    quickest_path= path_formatter(quickest['path'])[1]
    quickest_time = quickest['cost']



    shortest = dijkstra_path(network,dep,dest,cost_function=lambda u,v: specialized_geo_distance(network,u,v))
    formatted_short_path = path_formatter(shortest['path'])[0]
    shortest_path = path_formatter(shortest['path'])[1]
    shortest_distance = shortest['cost']


    timepath = "Quickest: " + " - ".join(formatted_quick_path) + f" - {quickest_time} minutes"
    geopath = "Shortest: " + " - ".join(formatted_short_path) + f" - {round(shortest_distance,3)} km"

    def colors(v):
        if (v in shortest_path and v in quickest_path):
            return "cyan"
        elif v in shortest_path:
            return "#90EE90"
        elif v in quickest_path:
            return "orange"
        else:
            return "white"

    color_svg_network(colormap=colors)
    
    return timepath, geopath



