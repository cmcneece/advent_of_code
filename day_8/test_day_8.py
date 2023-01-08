from .day_8 import part_1, part_2, get_forest_data
import numpy as np


def setup() -> np.array:
    ''' Returns the forest data '''
    input_path = 'test_input.txt'
    forest_data = get_forest_data(input_path)

    return forest_data


def test_part_1() -> bool:
    ''' Test part 1'''
    true_answer = 21
    forest_data = setup()
    assert true_answer == part_1(forest_data)


def test_part_2() -> bool:
    ''' Test part 2 '''
    true_answer = 8
    forest_data = setup()
    assert true_answer == part_2(forest_data)
