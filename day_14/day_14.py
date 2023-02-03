import pathlib
import os
from collections import namedtuple
import numpy as np
from typing import Union


DIR_PATH = pathlib.Path(__file__).parent.resolve()

START_IND = (0, 500)

Path = namedtuple('Path', ['x', 'y'])


def min_value_position(input: list[int]) -> tuple[int, int]:
    '''Return the min and index of a list'''
    min_val = min(input)
    return min_val, input.index(min_val)


def max_value_position(input: list[int]) -> tuple[int, int]:
    '''Return the max and index of a list'''
    max_val = max(input)
    return max_val, input.index(max_val)


def find_grain(domain: np.ndarray) -> tuple[int, int]:
    '''Find the falling grain in the domain, return the index'''
    grain_row, grain_col = np.where(domain == "+")
    grain_row = grain_row[0]
    grain_col = grain_col[0]
    return (grain_row, grain_col)


def check_move(domain: np.ndarray, grain_ind: tuple[int, int]) ->  Union[tuple[int, int], bool, str]:
    '''Checks the position of the falling sand grain and return the next move'''
    grain_row = grain_ind[0]
    grain_col = grain_ind[1]

    below_index = (grain_row+1, grain_col)
    down_left_index = (grain_row+1, grain_col-1)
    down_right_index = (grain_row+1, grain_col+1)

    try:
        if domain[below_index] == ".":
            return below_index
        elif domain[down_left_index] == ".":
            return down_left_index
        elif domain[down_right_index] == ".":
            return down_right_index
        else:   
            return "next"
    except:
        return False


def extract_paths(data: list[str]) -> tuple[list[int]]:
    '''Create the wall paths from the input data'''
    paths = []
    for line in data:
        path_parts = line.split(" -> ")
        xs = []
        ys = []
        for part in path_parts:
            x, y = part.split(",")
            xs.append(int(x))
            ys.append(int(y))
        paths.append(Path(x=xs, y=ys))

    paths_x = []
    paths_y = []
    for path in paths:
        for id, (x, y) in enumerate(zip(path.x[:-1], path.y[:-1])):
            x_diff = path.x[id+1] - x
            y_diff = path.y[id+1] - y
            run_length = max(abs(x_diff), abs(y_diff))
            if y_diff:
                for i in range(run_length+1):
                    paths_y.append(y+(i*np.sign(y_diff)))
                    paths_x.append(x)
            else:
                for i in range(run_length+1):
                    paths_x.append(x+(i*np.sign(x_diff)))
                    paths_y.append(y)
    return (paths_x, paths_y)


def make_domain_part_1(paths_x: list[int], paths_y: list[int]) -> tuple[np.ndarray, tuple[int, int]]:
    ''' Create the cavern domain from the paths we know about and the starting index'''
    x_dim = max(paths_x) - min(paths_x)
    y_dim = max(paths_y)
    domain = np.empty(shape=(y_dim+1, x_dim+1), dtype=str)
    domain[:][:] = "."
    for row, col in zip(paths_y, paths_x-min(paths_x)):
        domain[row, col] = "#"
    start_ind = (START_IND[0], START_IND[1]-min(paths_x))
    return domain, start_ind


def make_domain_part_2(paths_x: list[int], paths_y: list[int]) -> tuple[np.ndarray, tuple[int, int]]:
    ''' Create the updated cavern from the paths we know about and the starting index'''
    domain, start_ind = make_domain_part_1(paths_x=paths_x, paths_y=paths_y)
    height = domain.shape[0] + 2
    x_min_val, x_min_index = min_value_position(paths_x)
    x_max_val, x_max_index = min_value_position(paths_x)
    x_min_val -= min(paths_x)
    x_max_val -= min(paths_x)

    distance_left = max(height,
                        x_min_val + (height - paths_y[x_min_index]))
    distance_right = max(height,
                         x_max_val + (height - paths_y[x_max_index])) + 1

    add_left = abs(distance_left - start_ind[1])
    add_right = abs(distance_right - (domain.shape[1] - start_ind[1]))
    new_width = add_left + domain.shape[1] + add_right

    left_array = np.empty(shape=(domain.shape[0], add_left), dtype=str)
    right_array = np.empty(shape=(domain.shape[0], add_right), dtype=str)
    bottom_array = np.empty(shape=(2, new_width), dtype=str)

    left_array[:, :] = "."
    right_array[:, :] = "."
    bottom_array[0, :] = "."
    bottom_array[1, :] = "#"

    start_ind = (start_ind[0], start_ind[1] + add_left)
    new_domain = np.append(np.append(np.append(left_array, domain, axis=1), right_array, axis=1), bottom_array, axis=0)

    return new_domain, start_ind


def fill_domain(domain: np.ndarray, start_ind: tuple[int, int]) -> tuple[np.ndarray, int]:
    ''' Iteratively fill up the cavern, return the final state of the domain
    and the grains of sand'''
    flag = True
    domain[start_ind] = "+"
    grain_ind = start_ind

    while flag:
        updated_index = check_move(domain, grain_ind)
        if domain[grain_ind] == "o":
            flag = False
            continue
        if updated_index == "next":
            domain[start_ind] = "+"
            domain[grain_ind] = "o"
            grain_ind = start_ind
            continue
        elif not updated_index:
            flag = False
            continue
        domain[updated_index] = "+"
        domain[grain_ind] = "."
        grain_ind = updated_index
    return domain, sum(sum(domain == "o"))


if __name__ == "__main__":

    # set-up
    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        data = f.read().split('\n')
    paths_x, paths_y = extract_paths(data)

    # part_1
    domain, start_ind = make_domain_part_1(paths_x=paths_x, paths_y=paths_y)
    domain, sand_ind = fill_domain(domain, start_ind)
    print("The solution to part 1 is", sand_ind)

    # part_2
    part_2_domain, start_ind = make_domain_part_2(paths_x=paths_x, paths_y=paths_y)
    part_2_domain, sand_ind = fill_domain(part_2_domain, start_ind)
    print("The solution to part 2 is", sand_ind)
