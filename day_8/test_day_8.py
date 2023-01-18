from .day_8 import part_1, part_2, get_forest_data
import numpy as np
import pathlib
import os


DIR_PATH = pathlib.Path(__file__).parent.resolve()


def set_up() -> np.array:
    ''' Returns the forest data '''
    INPUT_FILE = 'test_input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    forest_data = get_forest_data(INPUT_PATH)

    return forest_data


def test_part_1() -> bool:
    ''' Test part 1'''
    true_answer = 21
    forest_data = set_up()
    assert true_answer == part_1(forest_data)


def test_part_2() -> bool:
    ''' Test part 2 '''
    true_answer = 8
    forest_data = set_up()
    assert true_answer == part_2(forest_data)
