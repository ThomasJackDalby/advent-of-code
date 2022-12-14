# Advent Of Code 2022 - Puzzle 9
# https://adventofcode.com/2022/day/9
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-14 06:18:34.019468
import sys

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [(direction, int(amount)) for (direction, amount) in [line.split(" ") for line in lines]]

LOOKUP = {
    (-2, 0) : (-1, 0),
    (2, 0) : (1, 0),
    (0, -2) : (0, -1),
    (0, 2) : (0, 1),

    (2, 2) : (1, 1),
    (2, 1) : (1, 1),
    (1, 2) : (1, 1),
    (-2, 2) : (-1, 1),
    (-2, 1) : (-1, 1),
    (-1, 2) : (-1, 1),
    (2, -2) : (1, -1),
    (2, -1) : (1, -1),
    (1, -2) : (1, -1),
    (-2, -2) : (-1, -1),
    (-2, -1) : (-1, -1),
    (-1, -2) : (-1, -1),
}
for delta in ((i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]):
    LOOKUP[delta] = (0, 0) # no movement

MOVEMENTS = {
    "U" : (0, 1),
    "D" : (0, -1),
    "L" : (-1, 0),
    "R" : (1, 0),
}

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def move(direction):
    head = add(head, direction)
    delta = sub(head, tail)
    print(delta)

def part_1(instructions):
    head = (0, 0)
    tail = (0, 0)

    tail_positions = set()
    for direction, amount in instructions:
        head_movement = MOVEMENTS[direction]
        for _ in range(amount):
            head = add(head, head_movement)
            delta = sub(head, tail)
            tail_movement = LOOKUP[delta]
            tail = add(tail, tail_movement)
            tail_positions.add(tail)
    print("part 1", len(tail_positions))

def part_2(instructions, length=10):
    rope = [(0, 0)] * length
    tail_positions = set()
    for direction, amount in instructions:
        head_movement = MOVEMENTS[direction]
        for _ in range(amount):
            rope[0] = add(rope[0], head_movement)
            for i in range(1, length):
                delta = sub(rope[i-1], rope[i])
                part_movement = LOOKUP[delta]
                rope[i] = add(rope[i], part_movement)
            tail_positions.add(rope[-1])
    print("part 2", len(tail_positions))

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    instructions = load_file(file_path)
    part_1(instructions)
    part_2(instructions)
    
