import os

FILE_NAME = "data.txt"

def load_file(file_path):
    with open(file_path, "r") as file:
        line = file.readline()
        return [int(v) for v in line.split(",")]

def part_1(fish, days=80):
    fish = list(fish)
    for day in range(days):
        for i in range(len(fish)):
            v = fish[i]
            if v == 0:
                fish.append(8)
                v = 6
            else:
                v -= 1
            fish[i] = v
    print(len(fish))

def part_2(fish, days=80):
    fish = [sum(1 for f in fish if f == d) for d in range(10)]
    for day in range(days):
        breed = fish[0]
        for i in range(1, 10):
            fish[i-1] = fish[i]

        fish[8] += breed
        fish[6] += breed
    print(fish)
    print(sum(fish))

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    fish = list(load_file(file_path))
    part_1(fish)
    part_2(fish, 256)
