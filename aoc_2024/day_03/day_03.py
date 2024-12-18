import pathlib
import os

import re

DIR_PATH = pathlib.Path(__file__).parent.resolve()


def find_valid_muls(input):
    mul_pattern = "\bmul\b\(\d{1,3},\d{1,3}\)"
    matches = re.findall(mul_pattern, input)

    return matches


def part_1(reports):

    return None


def part_2(reports):

    return None


if __name__ == "__main__":

    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()


    # Part 1
    part_1_answer = part_1(data)
    part_1_msg = f"For Part 1 there are {part_1_answer} safe reports."
    print(part_1_msg)

    # Part 2
    part_2_answer = part_2()
    part_2_msg = f"For Part 2 there are {part_2_answer} safe reports."
    print(part_2_msg)
