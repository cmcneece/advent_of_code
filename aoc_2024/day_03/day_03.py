import pathlib
import os

import re

DIR_PATH = pathlib.Path(__file__).parent.resolve()

MUL_PATTERN = r"mul\(\d{1,3},\d{1,3}\)"
DIGIT_PATTERN = r"\d{1,3}"
DONT_PATTERN = r"don\'t\(\)"
DO_PATTERN = r"do\(\)"

FULL_INSTRUCTION_PATTERN = "|".join([MUL_PATTERN, DONT_PATTERN, DO_PATTERN])


def parse_memory_muls_only(input):
    matches = re.findall(MUL_PATTERN, input)
    return matches


def parse_memory_all(input):
    matches = re.findall(FULL_INSTRUCTION_PATTERN, input)
    return matches


def proccess_memory(memory):
    instructions = []
    for match in memory:
        pairs = re.findall(DIGIT_PATTERN, match)
        if pairs:
            instructions.append((int(pairs[0]), int(pairs[1])))
        else:
            instructions.append(match)

    return instructions


def execute_instructions(instructions):
    cum_sum = 0
    do = True
    for instruction in instructions:
        if instruction == "don't()":
            do = False
            continue
        if instruction == "do()":
            do = True
            continue
        if do:
            cum_sum += instruction[0] * instruction[1]

    return cum_sum


def part_1(input):
    memory = parse_memory_muls_only(input=input)
    instructions = proccess_memory(memory=memory)
    cum_sum = execute_instructions(instructions=instructions)

    return cum_sum


def part_2(input):
    memory = parse_memory_all(input=input)
    instructions = proccess_memory(memory=memory)
    cum_sum = execute_instructions(instructions=instructions)

    return cum_sum


if __name__ == "__main__":

    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        input = f.read()

    # Part 1
    part_1_answer = part_1(input)
    part_1_msg = f"You get {part_1_answer} if you add up all of the results\
        of the multiplications."
    print(part_1_msg)

    # Part 2
    part_2_answer = part_2(input)
    part_2_msg = f"You get {part_2_answer} if you add up all of the results\
        of the multiplications."
    print(part_2_msg)
