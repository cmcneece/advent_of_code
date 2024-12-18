import pytest  # type: ignore
import pathlib
import os
from .day_02 import part_1, part_2, get_reports

DIR_PATH = pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def data():
    INPUT_FILE = 'test_input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()
    return get_reports(data)


def test_part_1(data):
    true_answer = 2
    part_1_answer = part_1(data)
    assert part_1_answer == true_answer


def test_part_2(data):
    true_answer = 4
    part_2_answer = part_2(data)
    assert part_2_answer == true_answer
