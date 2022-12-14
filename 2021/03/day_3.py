

FILE_PATH = "./day_3.txt"

def part_1(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    
    gamma = [1 if sum(1 for line in lines if line[i] == "1") > len(lines) // 2 else 0 for i in range(len(lines[0]))]
    epsilon = [abs(bit-1) for bit in gamma]
    gamma = convert_binary_to_int(gamma)
    epsilon = convert_binary_to_int(epsilon)
    return gamma, epsilon

def part_2(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    def search(lines, most_common=True):
        a, b = ("1", "0") if most_common else ("0", "1")
        i = 0
        while len(lines) > 1:
            count = sum(1 for line in lines if line[i] == "1")
            bit = a if count >= len(lines) / 2.0 else b
            print(count, len(lines) / 2.0, bit)
            lines = [line for line in lines if line[i] == bit]
            i += 1
        return lines[0]

    oxygen_gen = search(lines, True)
    c02_scrub = search(lines, False)

    oxygen_gen = convert_binary_to_int(oxygen_gen)
    c02_scrub = convert_binary_to_int(c02_scrub)

    return oxygen_gen, c02_scrub

def convert_binary_to_int(binary):
    return sum((pow(2, i) for i, v in enumerate(reversed(binary)) if int(v) == 1))

if __name__ == "__main__":

    oxygen_gen, c02_scrub = part_2(FILE_PATH)
    print(oxygen_gen, c02_scrub)
    print(oxygen_gen * c02_scrub)


    