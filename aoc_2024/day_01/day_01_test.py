from .day_01 import part_1, part_2
import pathlib
import os


DIR_PATH = pathlib.Path(__file__).parent.resolve()


def set_up():
    INPUT_FILE = 'test_input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()

    return data


def test_part_1(data):
    true_answer = 11

    part_1_answer = part_1(data, verbose=False)

    assert part_1_answer == true_answer


def test_part_2(data):
    true_answer = 31
    part_2_answer = part_2(data, verbose=False)
    assert part_2_answer == true_answer
