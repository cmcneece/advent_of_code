import pathlib
import os

import re

DIR_PATH = pathlib.Path(__file__).parent.resolve()

XMAS_PATTERN = r"XMAS"
SAMX_PATTERN = r"SAMX"


def find_xmas(input):
    count = 0
    for row in input:
        xmas_matches = re.findall(XMAS_PATTERN, row)
        samx_matches = re.findall(SAMX_PATTERN, row)
        count += len(xmas_matches + samx_matches)
    return count


def horizontal_unwrap(puzzle):
    return puzzle


def vertical_unwrap(puzzle):
    unpack_transpored = list(map(list, zip(*puzzle)))
    packed_transposed = []
    for row in unpack_transpored:
        packed_transposed.append("".join(row[:]))
    return packed_transposed


def diagonal_unwrap(puzzle):
    unpacked = list(map(list, puzzle))
    row_count = len(unpacked)
    col_count = len(unpacked[0])

    packed = []
    row_index = range(0, row_count)
    col_index = range(0, col_count)

    # lower left - southeast direction
    for row in range(0, row_count):
        packed.append([unpacked[i+row][j] for
                       i, j in zip(row_index, col_index) if
                       (j <= col_count-1) & (i+row <= row_count-1)])

    # upper right - southeast direction
    for col in range(1, col_count):
        packed.append([unpacked[i][j+col] for
                       i, j in zip(row_index, col_index) if
                       (j+col <= col_count-1) & (i <= row_count-1)])

    row_index = range(row_count-1, -1, -1)
    col_index = range(0, col_count, 1)

    # lower left - northeast direction
    for row in range(0, row_count):
        packed.append([unpacked[i-row][j] for
                       i, j in zip(row_index, col_index) if
                       (j <= col_count-1) & (i-row >= 0)])

    # upper right - northeast direction
    for col in range(1, col_count):
        packed.append([unpacked[i][j+col] for
                       i, j in zip(row_index, col_index) if
                       (j+col <= col_count-1) & (i >= 0)])

    joined = ["".join(row) for row in packed]

    return joined


def part_1(puzzle):
    horizontal_puzzle = horizontal_unwrap(puzzle)
    vertical_puzzle = vertical_unwrap(puzzle)
    diagonal_puzzle = diagonal_unwrap(puzzle)

    horizontal_count = find_xmas(horizontal_puzzle)
    vertical_count = find_xmas(vertical_puzzle)
    diagonal_count = find_xmas(diagonal_puzzle)

    total_count = horizontal_count + vertical_count + diagonal_count

    return total_count


# def part_2(input):
#     memory = parse_memory_all(input=input)
#     instructions = proccess_memory(memory=memory)
#     cum_sum = execute_instructions(instructions=instructions)

#     return cum_sum


if __name__ == "__main__":

    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        input = f.read().splitlines()

    # Part 1
    part_1_answer = part_1(input)
    part_1_msg = f"XMAS appears {part_1_answer} times."
    print(part_1_msg)

    # # Part 2
    # part_2_answer = part_2(input)
    # part_2_msg = f"XMAS appears {part_2_answer} times."
    # print(part_2_msg)
