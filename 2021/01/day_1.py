
def part_1(depths):
    total = 0
    previous_depth = None
    for depth in depths:
        if previous_depth is not None and depth > previous_depth:
            total += 1
        previous_depth = depth
    return total

def part_2(depths):
    previous_depth = None
    total = 0
    for i in range(2, len(depths)):
        depth = depths[i] + depths[i-1] + depths[i-2]   
        if previous_depth is not None and depth > previous_depth:
            total += 1
        previous_depth = depth
    return total

if __name__ == "__main__":
    with open("day_1.txt", "r") as file:
        lines = file.readlines()

    depths = [int(line.strip()) for line in lines]
    
    print(part_1(depths))
    print(part_2(depths))