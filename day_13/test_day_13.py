from .day_13 import part_1, part_2, get_pairs
import pathlib
import os

DIR_PATH = pathlib.Path(__file__).parent.resolve()


def set_up() -> tuple[list[list, int]]:
    ''' sets up the input tests'''
    INPUT_FILE = 'test_input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        data = f.read().split('\n')
    return get_pairs(data)


def test_part_1():
    ''' Tests part 1'''
    part_1_true_answer = 13
    pairs = set_up()
    part_1_solution = part_1(pairs)

    assert part_1_solution == part_1_true_answer


def test_part_2():
    ''' Tests part 2'''
    part_2_true_answer = 140
    pairs = set_up()
    part_2_solution = part_2(pairs)

    assert part_2_solution == part_2_true_answer
