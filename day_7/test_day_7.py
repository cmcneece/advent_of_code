from .day_7 import create_file_system, get_folder_sizes, part_1, part_2


def setup():
    input_path = 'test_input.txt'
    with open(input_path, 'r') as f:
        data = f.read().splitlines()

    file_system = create_file_system(data)
    folder_sizes = get_folder_sizes(file_system)

    return file_system, folder_sizes


def test_part_1():
    _, folder_sizes = setup()
    true_answer = 95437

    part_1_answer = part_1(folder_sizes)

    assert part_1_answer == true_answer


def test_part_2():
    file_system, folder_sizes = setup()
    true_answer = 24933642
    part_2_answer = part_2(file_system, folder_sizes)
    assert part_2_answer == true_answer


if __name__ == "__main__":

    folder_size = setup()
    test_part_1()
    test_part_2()
