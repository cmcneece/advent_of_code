import pytest  # type: ignore
import pathlib
import os
from .day_03 import part_1, part_2

DIR_PATH = pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def part_1_data():
    INPUT_FILE = 'test_input_part_1.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        part_1_data = f.read()
    return part_1_data


@pytest.fixture
def part_2_data():
    INPUT_FILE = 'test_input_part_2.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        part_2_data = f.read()
    return part_2_data


def test_part_1(part_1_data):
    true_answer = 161
    part_1_answer = part_1(part_1_data)
    assert part_1_answer == true_answer


def test_part_2(part_2_data):
    true_answer = 48
    part_2_answer = part_2(part_2_data)
    assert part_2_answer == true_answer
