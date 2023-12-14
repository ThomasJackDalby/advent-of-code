# Advent Of Code 2023 - Puzzle 5
# https://adventofcode.com/2023/day/5
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-06 06:23:00.762086

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 5

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/5/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

class MappingTable:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.ranges = []

    def convert(self, value, reverse=False):
        range = self.find_mapping_range(value, reverse)
        return range.convert(value, reverse) if range is not None else value
    
    def convert_range(self, value_range):
        value, length = value_range
        mapping_range = self.find_mapping_range(value)
        if mapping_range is not None:
            if mapping_range.contains(value + length):
                yield (mapping_range.convert(value), length)
            else:
                offset = mapping_range.source_max - value
                yield (mapping_range.convert(value), offset)
                for converted_range in self.convert_range((mapping_range.source_max, length - offset)):
                    yield converted_range
        else:
            mapping_range = next(filter(lambda range: range.source_min >= value, self.ranges), None)
            if mapping_range is None:
                yield value_range
            else:
                if not mapping_range.contains(value):
                    yield value_range
                else:
                    yield (value, mapping_range.source_min - value)
                    for converted_range in self.convert_range((mapping_range.source_max, length - offset)):
                        yield converted_range

    def find_mapping_range(self, value, reverse=False):
        return next(filter(lambda range: range.contains(value, reverse), self.ranges), None)

    def __str__(self) -> str:
        formatted_ranges = '\n'.join(str(r) for r in self.ranges)
        return f"[{self.source} to {self.target}]\n{formatted_ranges}"

class MappingRange:
    def __init__(self, source_min, target_min, length):
        self.source_min = source_min
        self.target_min = target_min
        self.length = length
    
        self.source_max = self.source_min + length
        self.target_max = self.target_min + length
        self.offset = self.target_min - self.source_min
    
    def contains(self, value, reverse=False):
        if not reverse: return self.source_min <= value and self.source_max > value
        return self.target_min <= value and self.target_max > value
    
    def convert(self, value, reverse=False):
        return value + (self.offset * (-1 if reverse else 1))

    def __str__(self) -> str:
        return f"{self.source_min}-{self.source_max} to {self.target_min}-{self.target_max} [{self.offset}]"

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = iter((line.strip() for line in file.readlines()))
    seed_line = next(lines)
    seeds = [int(s.strip()) for s in seed_line.strip().split(":")[1].strip().split(" ")]

    next(lines) # skip a line
    mapping_tables = []
    while True:
        header_line = next(lines, None)
        if header_line is None: break
        source, target = header_line.split(" ")[0].split("-to-")
        mapping_table = MappingTable(source, target)
        while True:
            line = next(lines, None)
            if line == "" or line is None: break
            target_min, source_min, length = (int(a) for a in line.split(" "))
            mapping_table.ranges.append(MappingRange(source_min, target_min, length))
        mapping_tables.append(mapping_table)
    return seeds, mapping_tables

def merge_maps(source_map, target_map):
    print("Merging")

    def format_range(range):
        return f"{range[0]} to {range[0]+range[2]} {range[1]} to {range[1]+range[2]} [{range[2]}]"

    def print_range(range):
        print(format_range(range))

    def print_map(map):
        print(f"{map[0][0]} to {map[0][1]}")
        for range in map[1]: print_range(range)

    print_map(source_map)
    print_map(target_map)

    merged_map = []
    ordered_source_ranges = list(sorted((source_range for source_range in source_map[1]), key=lambda r: r[1]))
    ordered_target_ranges = list(sorted((target_range for target_range in target_map[1]), key=lambda r: r[0]))

    for source_range in ordered_source_ranges:
        print(f"{source_range=}")
        value = source_range[1]
        while value < source_range[1] + source_range[2]:
            print(f"{value=}")
            target_range = next((r for r in ordered_target_ranges if r[0] <= value and value < r[0] + r[2]), None)
            if target_range is None:
                next_target_range = next((r for r in ordered_target_ranges if r[0] > value), None)
                if next_target_range is None:
                    end = source_range[1] + source_range[2]
                    updated_range = (source_range[0]+source_range[2]-end+value,value, end - value)
                    value = end
                    merged_map.append(updated_range)
                else:
                    print(f"No range for {value} so equal. Next range is {format_range(next_target_range)}")
                    value = target_range[0]
            else:
                print(f"Found target range {format_range(target_range)}")
                end = min(source_range[1] + source_range[2], target_range[0]+target_range[2])
                updated_range = (value, value, end - value)
                merged_map.append(updated_range)
                value = end

            print(f"{updated_range=}")
    return merged_map

def part_1(data):
    values, tables = data
    current = "seed"
    while current != "location":
        table = next(filter(lambda t: t.source == current, tables))
        values = [table.convert(value) for value in values]
        current = table.target
    result = min(values)
    print(f"part 1: {result}")
    
def part_2(data):
    values, tables = data
    value_ranges = [(values[i], values[i+1]) for i in range(0, len(values), 2)]
    current = "seed"
    while current != "location":
        table = next(filter(lambda t: t.source == current, tables))
        value_ranges = [converted_value_range for value_range in value_ranges for converted_value_range in table.convert_range(value_range)]
        current = table.target
    result = min((value for value, _ in value_ranges))
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)