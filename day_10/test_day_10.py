from .day_10 import part_1


def test_part_1():
    part_1_true_answer = 13140
    INPUT_PATH = 'part_1_test_input.txt'

    with open(INPUT_PATH, 'r') as f:
        instructions = [line.strip().split() for line in f.readlines()]

    part_1_answer = part_1(instructions)
    assert part_1_true_answer == part_1_answer
