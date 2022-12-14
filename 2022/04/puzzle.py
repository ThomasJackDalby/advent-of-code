# Advent Of Code 2022 - Puzzle 4
# https://adventofcode.com/2022/day/4
# Tom Dalby - https://github.com/thomasjackdalby

import sys

file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
with open(file_path, "r") as file:
    lines = [line.strip() for line in file.readlines()]

def parse_zones(zones):
    return tuple((int(zone) for zone in zones.split("-")))

def parse_line(line):
    return tuple((parse_zones(zones) for zones in line.split(",")))

def check_fully_contains(line):
    left, right = parse_line(line)
    if left[0] <= right[0] and left[1] >= right[1]:
        return True
    elif right[0] <= left[0] and right[1] >= left[1]:
        return True
    else:
        return False

score = sum((1 for line in lines if check_fully_contains(line)))
print("part 1", score)

def is_between(value, min, max):
    return value >= min and value <= max

def check_overlap(line):
    left, right = parse_line(line)
    if is_between(left[0], right[0], right[1]):
        return True
    if is_between(left[1], right[0], right[1]):
        return True
    if is_between(right[0], left[0], left[1]):
        return True
    if is_between(right[1], left[0], left[1]):
        return True
    return False

score = sum((1 for line in lines if check_overlap(line)))
print("part 2", score)
