# Advent Of Code 2022 - Puzzle 8
# https://adventofcode.com/2022/day/8
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-13 21:43:07.696831
import sys

def load_file(file_path):
    with open(file_path, "r") as file:
        return [[int(tree) for tree in line.strip()] for line in file.readlines()]

def print_visibility_grid(grid):
    for row in grid:
        print("".join("1" if tree else "." for tree in row))

def create_grid(number_of_rows, number_of_columns, default_value):
    return  [[default_value for _ in range(number_of_columns)] for _ in range(number_of_rows)]

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

    height_grid = load_file(file_path)
    number_of_rows = len(height_grid)
    number_of_columns = len(height_grid[0])

    visibility_grid = create_grid(number_of_rows, number_of_columns, False)
    left_to_right = [[(r, c) for c in range(number_of_columns)] for r in range(number_of_rows)]
    right_to_left = [[(r, c) for c in range(number_of_columns-1, -1, -1)] for r in range(number_of_rows)]
    top_to_bottom = [[(r, c) for r in range(number_of_rows)] for c in range(number_of_columns)]
    bottom_to_top = [[(r, c) for r in range(number_of_rows-1, -1, -1)] for c in range(number_of_columns)]

    def check_grid(coordinates):
        for row in coordinates:
            height = -1
            for r, c in row:
                if height_grid[r][c] > height:
                    visibility_grid[r][c] = True
                    height = height_grid[r][c]

    check_grid(left_to_right)
    check_grid(right_to_left)
    check_grid(top_to_bottom)
    check_grid(bottom_to_top)

    print("part 1", sum((1 for row in visibility_grid for tree in row if tree)))

    # brute force
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    scenic_grid = create_grid(number_of_rows, number_of_columns, 0)
    max_scenic_score = 0
    for r in range(number_of_rows):
        for c in range(number_of_columns):
            height = height_grid[r][c]
            score = 1
            for x, y in DIRECTIONS:
                distance = 1
                d_score = 0
                while True:
                    y_i = r + y * distance
                    x_i = c + x * distance
                    if y_i < 0 or y_i >= number_of_rows:
                        d_score = distance - 1
                        break
                    if x_i < 0 or x_i >= number_of_columns:
                        d_score = distance - 1
                        break

                    h = height_grid[r + y * distance][c + x * distance]
                    if h >= height:
                        d_score = distance
                        break
                    distance += 1
                score *= d_score
            scenic_grid[r][c] = score
            if score > max_scenic_score:
                max_scenic_score = score
    print("part 2", max_scenic_score)
    # print("\n".join(" ".join(str(tree).rjust(2) for tree in row) for row in scenic_grid))





    
    
    
    

