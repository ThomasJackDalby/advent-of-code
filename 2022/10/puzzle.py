# Advent Of Code 2022 - Puzzle 10
# https://adventofcode.com/2022/day/10
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-14 18:55:28.591863
import sys

def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.strip().split() for line in lines]

def process(commands, signals):

    commands = iter(commands)
    x_value = 1
    cycle = 0
    command_duration = 0
    command_action = None
    total = 0
    pixels = ["."]*240

    while True:
        if cycle in signals:
            total += x_value * cycle
        
        # get next command
        if command_duration == 0:
            command, *args = next(commands, [None])
            if command is None:
                break
            if command == "addx":
                command_duration = 2
                def assign_x():
                    nonlocal x_value
                    x_value += int(args[0])
                command_action = assign_x
            elif command == "noop":
                command_duration = 1

        # draw the pixel
        pixel_index = cycle % 40
        if x_value in [pixel_index-1, pixel_index, pixel_index+1]:
            pixels[cycle] = "#"

        command_duration -= 1
        cycle += 1

        if command_duration == 0 and command_action is not None: # occurs at end of cycle
            command_action()
            command_action = None

    return total, pixels

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    commands = read_file(file_path)
    score, pixels = process(commands, [20, 60, 100, 140, 180, 220])
    print("part 1", score)

    for i in range(6):
        print("".join(pixels[i*40:(i+1)*40]))
