# Advent Of Code 2022 - Puzzle 15
# https://adventofcode.com/2022/day/15
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-27 20:07:52.548467

import sys
import re
import aocd
from itertools import groupby

PATTERN = '=-?\d+'

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def get_distance_between(a, b):
    delta = sub(b, a)
    return abs(delta[0]) + abs(delta[1])

class Sensor:
    def __init__(self, position, nearest_beacon_position):
        self.position = position
        self.nearest_beacon_position = nearest_beacon_position
        self.range = get_distance_between(self.position, self.nearest_beacon_position)
        print(f"Sensor @ {self.position} {self.nearest_beacon_position} [{self.range}]")

    def in_range(self, position):
        return get_distance_between(position, self.position) <= self.range

    def get_y_range(self, x):
        x_delta = abs(self.position[0] - x)
        y_delta = self.range - x_delta
        return y_delta

    def get_x_range(self, y):
        y_delta = abs(self.position[1] - y)
        x_delta = self.range - y_delta
        return x_delta

def load_data(file_path):
    with open(file_path, "r") as file:
        return file.read()

def parse_data(data):
    lines = [line.strip() for line in data.split("\n")]
    lines = [[int(match[1:]) for match in re.findall(PATTERN, line)] for line in lines]
    return [Sensor((line[0], line[1]), (line[2], line[3])) for line in lines]

# def search_y(sensors, y):
#     y = 2000000
#     total = 0
#     for x in range(min_x, max_x+1):
#         position = (x, y)
#         in_range = False
#         if any(sensor.nearest_beacon_position == position for sensor in sensors):
#             continue
#         for sensor in sensors:
#             if get_distance_between(sensor.position, position) <= sensor.range:
#                 in_range = True
#                 break
#         if in_range:
#             total += 1

check_count = 0

def search_y(sensors, min_x, max_x, y, y_cache):
    global check_count
    x = min_x
    while x <= max_x:
        if y < y_cache[x - min_x]:
            x += 1
            continue

        position = (x, y)

        # check if any sensor in range
        sensor = next((sensor for sensor in sensors if sensor.in_range(position)), None)
        if sensor is None:
            print(f"No sensors in range at {position}!")
            return (x, y)

        # update the y-cache
        y_cache[x - min_x] = sensor.position[1] + sensor.get_y_range(x) + 1
        
        # skip to edge of sensor range
        x = sensor.position[0] + sensor.get_x_range(y) + 1
    return None

def search_xy(sensors, min_x, min_y, max_x, max_y):

    y_cache = [0] * (max_y - min_y + 1)

    for y in range(min_y, max_y+1):
        result = search_y(sensors, min_x, max_x, y, y_cache)
        if result is not None:
            return result
    return None

def create_sensor_grid(sensors):
    # returns a grid of non-overlapping cells where each cell is completely within a distinct set of sensors
    # allows each cell to only search the sub-set of sensors
    # each sensor has a min/max x/y
    # each min/max x/y forms the edge of a cell

    def partition(items, get_value):
        sorted_items = list(sorted(((get_value(item, state), state, item) for item in items for state in [True, False]), key=lambda s: s[0]))   
        print("sorted")
        for item in sorted_items:
            print(item)
        print("/sorted")

        actions = list(groupby(sorted_items, key=lambda y: y[0]))
        current_items = []
        print(len(actions), len(sorted_items))
        for i, (value, actions) in enumerate(actions[:-1]):
            print(f"{i=} {value=} {len(list(actions))=}")
            for state, item in actions:
                print(state, item)

                if state: current_items.append(item)
                else: current_items.remove(item)

                min_value = value
                max_value = actions[i+1][0]
                yield ((min_value, max_value), list(current_items))

    grid = []
    for (y_min, y_max), y_sensors in partition(sensors, lambda sensor, state: sensor.position[1] + sensor.range * (1 if state else -1)):
        for (x_min, x_max), x_sensors in partition(y_sensors, lambda sensor, state: sensor.position[0] + sensor.range * (1 if state else -1)):
            grid.append((x_min, y_min, x_max, y_max), list(x_sensors))
    return grid

def print_sensors(sensors, min_x, min_y, max_x, max_y):

    def get_char(position):
        char = ' '
        for sensor in sensors:
            delta = get_distance_between(position, sensor.position)
            if delta == 0:
                return 'S'
            if position == sensor.nearest_beacon_position:
                return 'B'
            elif char == ' ' and delta <= sensor.range:
                char = '#'
        return char

    for y in range(min_y, max_y+1):
        chars = [get_char((x, y)) for x in range(min_x, max_x+1)]
        line = "".join(chars)
        print(line)

if __name__ == "__main__":
    if len(sys.argv) < 2: data = aocd.get_data(day=15, year=2022)
    else: data = load_data(sys.argv[1])
    sensors = parse_data(data)

    # part 1
    print(">>>>>>>>")
    for (x_min, y_min, x_max, y_max), sensors in create_sensor_grid(sensors):
        print(x_min, y_min, x_max, y_max, len(sensors))
    print(">>>>>>>>")
    
    exit()

    # part 2
    position = search_xy(sensors, 0, 0, 4000000, 4000000)
    if position is None:
        raise Exception("Can't find")
    
    x, y = position
    frequency = x * 4000000 + y
    print("part 2", frequency)