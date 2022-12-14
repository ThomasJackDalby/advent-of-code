# Advent Of Code 2022 - Puzzle 5
# https://adventofcode.com/2022/day/5
# Tom Dalby - https://github.com/thomasjackdalby

import sys

def read_input_file(file_path):
    print(f"Loading input file [{file_path}]")
    read_crates = True
    stacks = None
    instructions = []

    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    for line in lines:
        if len(line) == 0:
            continue
        if read_crates and len(line) > 0 and line[0] != "[":
            read_crates = False
        if not read_crates and line[0] != "m":
            continue

        if stacks is None:
            number_of_stacks = (len(line)+1)//4
            stacks = [[] for i in range(number_of_stacks)]

        if read_crates:
            for i in range(number_of_stacks):
                if line[4*i + 1] != ' ':
                    stacks[i].append(line[4*i + 1])
        else:
            bits = line.split(' ')
            number_of_crates = int(bits[1])
            source = int(bits[3])
            target = int(bits[5])
            instructions.append((number_of_crates, source, target))
    
    print(f"Loaded {len(stacks)} stacks and {len(instructions)} instructions")
    return stacks, instructions

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    stacks, instructions = read_input_file(file_path)

    for instruction in instructions:
        number_of_crates, source, target = instruction
        picked_up = list(reversed(stacks[source-1][:number_of_crates]))
        stacks[source-1] = stacks[source-1][number_of_crates:]
        stacks[target-1] = picked_up + stacks[target-1]

result = "".join((stack[0] for stack in stacks))
print(result)