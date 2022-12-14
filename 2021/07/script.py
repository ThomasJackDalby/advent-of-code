import os

FILE_NAME = "data.txt"

def load_file(file_path):
    with open(file_path, "r") as file:
        line = file.readline()
        return [int(v) for v in line.split(",")]

def get_fuel(distance):
    return distance * (distance + 1) // 2

def part_1(crabs):
    positions = [0] * (max(crabs)+1)
    for crab in crabs:
        positions[crab] += 1
    min_fuel = None
    min_position = None    
    for target in range(len(positions)):
        fuel = 0
        for position, amount in enumerate(positions):
            distance = abs(target - position)
            fuel += amount * get_fuel(distance)
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
            min_position = position
    
    print(min_fuel, min_position)

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    crabs = list(load_file(file_path))
    part_1(crabs)