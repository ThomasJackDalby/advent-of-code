GROUPS = [
    [0, 1, 2, 3, 4],
    [5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24],
    [0, 5, 10, 15, 20],
    [1, 6, 11, 16, 21],
    [2, 7, 12, 17, 22],
    [3, 8, 13, 18, 23],
    [4, 9, 14, 19, 24],
]

def load_file(file_path):
    with open(file_path, "r") as file:       
        numbers = [int(number.strip()) for number in file.readline().split(",")]
        file.readline()

        bingo_cards = []
        while True:
            bingo_card = [number for _ in range(5) for number in (number.strip() for number in file.readline().strip().replace("  ", " ").split(" "))]
            if len(bingo_card) == 25:
                bingo_cards.append([int(number) for number in bingo_card])
                file.readline()
            else:
                return numbers, bingo_cards

def check_bingo_card(bingo_card, scratched_numbers):
    return any((all((scratched_numbers[bingo_card[cell]] for cell in group)) for group in GROUPS))

def get_winning_card(bingo_cards, scratched_numbers):
    for number in numbers:
        scratched_numbers[number] = True
        for bingo_card in bingo_cards:
            if (check_bingo_card(bingo_card, scratched_numbers)):
                return bingo_card, number

def part_1(numbers, bingo_cards):
    scratched_numbers = [False for _ in range(max(numbers) + 1)]
    bingo_card, number = get_winning_card(bingo_cards, scratched_numbers)
    return sum(bingo_card[cell] for cell in range(25) if not scratched_numbers[bingo_card[cell]]) * number

def part_2(numbers, bingo_cards):
    scratched_numbers = [False for _ in range(max(numbers) + 1)]
    while len(bingo_cards) > 0:
        bingo_card, number = get_winning_card(bingo_cards, scratched_numbers)
        bingo_cards.remove(bingo_card)
    return sum(bingo_card[cell] for cell in range(25) if not scratched_numbers[bingo_card[cell]]) * number

if __name__ == "__main__":
    numbers, bingo_cards = load_file("day_4.txt")
    print(part_1(numbers, bingo_cards))
    print(part_2(numbers, bingo_cards))
