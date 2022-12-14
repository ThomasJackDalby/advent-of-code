# Advent Of Code 2022 - Puzzle 6
# # https://adventofcode.com/2022/day/6
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 

def get_next_packet_start(buffer, length):
    index = length - 1
    packet = [next(buffer) for i in range(length)]
    while True:
        if len(set(packet)) == length:
            return index + 1
        index += 1
        packet[index % length] = next(buffer)

if __name__ == "__main__":
    import sys
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

    with open(file_path, "r") as file:
        buffer = file.readlines()[0]

    print("part 1", get_next_packet_start(iter(buffer), 4))
    print("part 2", get_next_packet_start(iter(buffer), 14))


