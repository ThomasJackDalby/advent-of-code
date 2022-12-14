import os

FILE_NAME = "data.txt"

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    for line in lines:
        bits = [int(v) for text in line.strip().split(" ")[0::2] for v in text.split(",")]
        yield bits

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def get_delta(start, end):
    x = sign(end[0] - start[0])
    y = sign(end[1] - start[1])
    return (x, y)

def part_1(vents, allow_diag=False):
    coords = {}
    for vent in vents:
        start = tuple(vent[0:2])
        end = tuple(vent[2:4])
        delta = get_delta(start, end)
        if not allow_diag and not (delta[0] == 0 or delta[1] == 0):
            continue

        current = start
        stop = add(end, delta)
        length = 0
        while current != stop:
            if current not in coords:
                coords[current] = 0
            coords[current] += 1
            length += 1
            current = add(current, delta)
    result = sum(1 for amount in coords.values() if amount > 1)
    print(f"{result=}")

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    vents = list(load_file(file_path))
    part_1(vents, False)
    part_1(vents, True)