
FORWARD = 0
UP = 1
DOWN = 2

def parse_command(command):
    char = command[0]
    if char == "f":
        return FORWARD
    elif char == "u":
        return UP
    else:
        return DOWN

def parse_commands(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
    return [(parse_command(line[0]), int(line[1])) for line in lines]

def part_1(commands):
    position, depth = 0, 0
    for command, amount in commands:
        if command == FORWARD:
            position += amount
        elif command == UP:
            depth -= amount
        else:
            depth += amount
    return position * depth

def part_2(commands):
    position, depth, aim = 0, 0, 0
    for command, amount in commands:
        if command == FORWARD:
            position += amount
            depth += amount * aim
        elif command == UP:
            aim -= amount
        else:
            aim += amount
    return position * depth

if __name__ == "__main__":
    commands = parse_commands("day_2.txt")

    result = part_2(commands)

    print(result)
