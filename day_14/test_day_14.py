from .day_14 import extract_paths, make_domain_part_1, make_domain_part_2, fill_domain
import pathlib
import os

DIR_PATH = pathlib.Path(__file__).parent.resolve()


def set_up() -> tuple[list[int], list[int]]:
    ''' sets up the input tests'''
    INPUT_FILE = 'test_input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        data = f.read().split('\n')
    return extract_paths(data)


def test_part_1():
    ''' Tests part 1'''
    paths_x, paths_y = set_up()
    part_1_true_answer = 24
    domain, start_ind = make_domain_part_1(paths_x=paths_x, paths_y=paths_y)
    _, total_sand_grains = fill_domain(domain, start_ind)
    assert total_sand_grains == part_1_true_answer


def test_part_2():
    ''' Tests part 2'''
    paths_x, paths_y = set_up()
    part_2_true_answer = 93
    domain, start_ind = make_domain_part_2(paths_x=paths_x, paths_y=paths_y)
    _, total_sand_grains = fill_domain(domain, start_ind)
    assert total_sand_grains == part_2_true_answer
