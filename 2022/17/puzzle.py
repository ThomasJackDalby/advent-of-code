# Advent Of Code 2022 - Puzzle 17
# https://adventofcode.com/2022/day/17
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-01-09 10:22:56.058723
import sys

class BlockType:
    def __init__(self, shape):
        self.shape = shape
        self.height = len(shape)
        self.width = len(shape[0])

    def intersects(self, other):
        return False

class Block:
    def __init__(self, block_type) :
        self.block_type = block_type

BLOCKS = [
    BlockType([[1,1,1,1]]),
    BlockType([[0,1,0], [1,1,1], [0,1,1]]),
    BlockType([[0,0,1], [0,0,1], [1,1,1]]),
    BlockType([[1],[1],[1],[1]]),
    BlockType([[1,1],[1,1]]),
]

def load_file(file_path):
    with open(file_path, "r") as file:
        return [1 if c == ">" else -1 for c in file.read().strip()]

def get_top(block):
    return block[1]
def get_bottom(block):
    return block[1] - BLOCKS[block[2]]

def process(tower, winds):
    pass
    # tower is a list of tuples or the form (x, y, type)
    # the tower is 7 wide

    # block_type_index = 0

    # current_block = [2, 10, block_type_index]
    # for wind in winds:

    #     # move the block town


    #     # check intersections in a top down manner
    #     for block in reversed(tower):
    #         if get_top(block) < get_bottom(current_block) 


    # block = (x, y, block_type)


if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    wind = load_file(file_path)
    print(wind)