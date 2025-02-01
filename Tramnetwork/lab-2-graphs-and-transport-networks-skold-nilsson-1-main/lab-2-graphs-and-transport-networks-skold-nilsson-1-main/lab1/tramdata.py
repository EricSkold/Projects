import sys
import json
import math
import csv


# files given
STOP_FILE = "./data/tramstops.json"
LINE_FILE = "./data/tramlines.txt"

# file to give
TRAM_FILE = "./tramnetwork.json"


def build_tram_stops(jsonobject):
    with open(jsonobject, "r", encoding="utf-8") as data:
        input_data = json.load(data)
        return {
            key: {
                "lat": float(input_data[key]["position"][0]),
                "lon": float(input_data[key]["position"][1]),
            }
            for key in input_data
        }


def retrieve_data(file):
    with open(file, "r", encoding="utf-8") as data:
        input_data = list(csv.reader(data, delimiter=":"))
        stop_data = [
            [item.replace(" 10", "").strip() for item in ls if (item != "")]
            if not ls[0].isdigit()
            else ls[0]
            for ls in input_data
            if ls != []
        ]

        return stop_data, [stop_data.index(linje) for linje in stop_data if linje[0].isdigit()]


def build_tram_lines(lines):
    input_data = retrieve_data(lines)
    input_list = input_data[0]
    input_index_list = input_data[1]

    # Bygger line dictionary
    tram_lines = {
        input_list[input_index_list[n]]: [
            item[0]
            for item in input_list[input_index_list[n] + 1 : input_index_list[n + 1]]
        ]
        if n + 1 < len(input_index_list)
        else [item[0] for item in input_list[input_index_list[n] + 1 :]]
        for n in range(len(input_index_list))
    }

    # Bygger time dictionary
    transition_dict = {}
    for key in input_index_list[: len(input_index_list)]:
        stop_list = (
            input_list[key + 1 : input_index_list[input_index_list.index(key) + 1]]
            if input_index_list.index(key) < len(input_index_list) - 1
            else input_list[key + 1 :]
        )

        for stop in stop_list[: len(stop_list) - 1]:

            adjacent_stop = stop_list[stop_list.index(stop) + 1][0]

            transition_times = [
                int(stop_list[stop_list.index(stop)][1]),
                int(stop_list[stop_list.index(stop) + 1][1]),
            ]

            add_stop = {adjacent_stop: abs(transition_times[0] - transition_times[1])}

            if stop[0] not in transition_dict:
                if stop[0] not in transition_dict.get(adjacent_stop, {}).keys():
                    transition_dict[stop[0]] = add_stop

            else:
                if stop[0] not in transition_dict.get(adjacent_stop, {}).keys():
                    transition_dict[stop[0]].update(add_stop)

    return (tram_lines, transition_dict)


def build_tram_network(stopfile, linefile):
    conc_dict = {
        "stops": {**build_tram_stops(stopfile)},
        "lines": {**build_tram_lines(linefile)[0]},
        "times": {**build_tram_lines(linefile)[1]},
    }
    with open("tramnetwork.json", "w", encoding="utf-8") as output_file:
        json.dump(conc_dict, output_file, ensure_ascii=False, indent=4)


def lines_via_stop(linedict, stop):
    return [line for line in linedict if stop in linedict[line]]


def lines_between_stops(linedict, stop1, stop2):
    return [line for line in linedict if stop1 in linedict[line] and stop2 in linedict[line]]


def time_between_stops(linedict, timedict, line, stop1, stop2):
    if stop1 in linedict[line] and stop2 in linedict[line]:
        stop_index = [linedict[line].index(stop2), linedict[line].index(stop1)]

        return sum(sum(
                timedict[stop][key]
                for key in linedict[line][min(stop_index) : max(stop_index) + 1]
                if key in timedict[stop] and linedict[line].index(key) >= linedict[line].index(stop)-1
            )
            for stop in linedict[line][min(stop_index) : max(stop_index) + 1]
            if stop in timedict
        )
    else:
        return f"{stop1} and {stop2} are not along the same line!"


def distance_between_stops(stopdict, stop1, stop2):
    mean_latitude = math.radians((stopdict[stop1]["lat"] + stopdict[stop2]["lat"]) / 2)
    delta_latitude = math.radians(stopdict[stop1]["lat"] - stopdict[stop2]["lat"])
    delta_longitude = math.radians(stopdict[stop1]["lon"] - stopdict[stop2]["lon"])
    radius = 6371.009

    return round(radius* math.sqrt((delta_latitude**2) + (math.cos(mean_latitude) * delta_longitude) ** 2),3,)


# Returns value of type list, integer, float or boolean,
# hence our choice of -1 for the error "unknown argument".
def answer_query(tramdict, query):
    ans = False

    if query[:3] == "via":
        if query[4:] in tramdict["stops"]:
            ans = lines_via_stop(tramdict["lines"], query[4:])
        else:
            ans = -1

    elif query[:7] == "between" and " and " in query:
        stop_1 = query[8 : query.index(" and ")]
        stop_2 = query[query.index(" and ") + 5 :]

        if stop_1 in tramdict["stops"] and stop_2 in tramdict["stops"]:
            ans = lines_between_stops(tramdict["lines"], stop_1, stop_2)
        else:
            ans = -1

    elif query[:9] == "time with" and " from " in query and " to " in query:
        line_nr = query[10 : query.index(" from ")]
        stop_1 = query[query.index(" from ") + 6 : query.index(" to ")]
        stop_2 = query[query.index(" to ") + 4 :]

        if (
            line_nr in tramdict["lines"]
            and stop_1 in tramdict["stops"]
            and stop_2 in tramdict["stops"]
        ):
            ans = time_between_stops(
                tramdict["lines"], tramdict["times"], line_nr, stop_1, stop_2
            )

        else:
            ans = -1

    elif query[:13] == "distance from" and " to " in query:
        stop_1 = query[query.index(" from ") + 6 : query.index(" to ")]
        stop_2 = query[query.index(" to ") + 4 :]

        if stop_1 in tramdict["stops"] and stop_2 in tramdict["stops"]:
            ans = distance_between_stops(tramdict["stops"], stop_1, stop_2)
        else:
            ans = -1

    return ans


def dialogue(tramfile=TRAM_FILE):
    with open(tramfile, "r", encoding="utf-8") as network_data:
        data = json.load(network_data)

        while True:
            user_input = input("> ")
            if user_input != "quit":
                if answer_query(data, user_input) == -1:
                    print("unknown argument")
                elif answer_query(data, user_input) == False:
                    print("sorry, try again")
                else:
                    print(answer_query(data, user_input))
            else:
                break
            

if __name__ == "__main__":
    if sys.argv[1:] == ["init"]:
        build_tram_network(STOP_FILE, LINE_FILE)
    else:
        dialogue()
