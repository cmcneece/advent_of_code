from .day_7 import create_file_system, get_folder_sizes, part_1, part_2
import pathlib
import os


DIR_PATH = pathlib.Path(__file__).parent.resolve()


def set_up():
    INPUT_FILE = 'test_input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()

    file_system = create_file_system(data)
    folder_sizes = get_folder_sizes(file_system)

    return file_system, folder_sizes


def test_part_1():
    _, folder_sizes = set_up()
    true_answer = 95437

    part_1_answer = part_1(folder_sizes)

    assert part_1_answer == true_answer


def test_part_2():
    file_system, folder_sizes = set_up()
    true_answer = 24933642
    part_2_answer = part_2(file_system, folder_sizes)
    assert part_2_answer == true_answer


if __name__ == "__main__":

    folder_size = set_up()
    test_part_1()
    test_part_2()
