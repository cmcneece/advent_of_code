import pathlib
import os
import numpy as np
from typing import Union


DIR_PATH = pathlib.Path(__file__).parent.resolve()

START_IND = (0, 500)


def min_value_position(input: list[int]) -> tuple[int, int]:
    '''Return the min and index of a list'''
    min_val = min(input)
    return min_val, input.index(min_val)


def max_value_position(input: list[int]) -> tuple[int, int]:
    '''Return the max and index of a list'''
    max_val = max(input)
    return max_val, input.index(max_val)


def check_move(domain: np.ndarray, grain_ind: tuple[int, int]) ->  Union[tuple[int, int], bool, str]:
    '''Checks the position of the falling sand grain and return the next move'''

    below_index = (grain_ind[0]+1, grain_ind[1])
    down_left_index = (grain_ind[0]+1, grain_ind[1]-1)
    down_right_index = (grain_ind[0]+1, grain_ind[1]+1)

    try:
        # if the spaces are anything but "." then the grain cant move there
        if domain[below_index] == ".":
            return below_index
        if domain[down_left_index] == ".":
            return down_left_index
        if domain[down_right_index] == ".":
            return down_right_index
        return "next"
    except IndexError:
        # if the above fails then the grain falls out of the domain
        return False


def extract_paths(data: list[str]) -> tuple[list[int]]:
    '''Create the wall paths from the input data'''
    # pull out the verticies of each path from the input data
    path_verticies = []
    for line in data:
        path_parts = line.split(" -> ")
        xs = []
        ys = []
        for part in path_parts:
            x, y = part.split(",")
            xs.append(int(x))
            ys.append(int(y))
        path_verticies.append([xs, ys])

    # interpolate the paths from the verticies
    path_xs = []
    path_ys = []
    for path in path_verticies:
        # iterate through each path
        x_verticies = path[0]
        y_verticies = path[1]
        for id, (x, y) in enumerate(zip(x_verticies[:-1], y_verticies[:-1])):
            # iterate through each vertex in the path

            # determine the deltas and run length for interpolation
            x_diff = x_verticies[id+1] - x
            y_diff = y_verticies[id+1] - y
            run_length = max(abs(x_diff), abs(y_diff)) + 1

            # create the full paths
            if y_diff:
                for i in range(run_length):
                    path_ys.append(y + (i * np.sign(y_diff)))
                    path_xs.append(x)
            else:
                for i in range(run_length):
                    path_xs.append(x + (i * np.sign(x_diff)))
                    path_ys.append(y)
    return (path_xs, path_ys)


def make_domain_part_1(path_xs: list[int], path_ys: list[int]) -> tuple[np.ndarray, tuple[int, int]]:
    ''' Create the cavern domain from the paths we know about and the starting index'''
    # find the domain size based on the paths
    x_dim = max(path_xs) - min(path_xs) + 1
    y_dim = max(path_ys) + 1
    domain = np.empty(shape=(y_dim, x_dim), dtype=str)

    # empty space everywhere except the paths
    domain[:][:] = "."
    for row, col in zip(path_ys, path_xs-min(path_xs)):
        domain[row, col] = "#"

    # reindex the starting index given the domain size
    start_ind = (START_IND[0], START_IND[1]-min(path_xs))
    return (domain, start_ind)


def make_domain_part_2(path_xs: list[int], path_ys: list[int]) -> tuple[np.ndarray, tuple[int, int]]:
    ''' Create the updated cavern from the paths we know about and the starting index'''

    # leverage the original domain logic then add the additional space required
    domain, start_ind = make_domain_part_1(path_xs=path_xs, path_ys=path_ys)

    # bottom of the cavern is 2 below lowest path
    height = domain.shape[0] + 2

    # find the leftmost and rightmost paths and reindex
    x_min_val, x_min_index = min_value_position(path_xs)
    x_max_val, x_max_index = min_value_position(path_xs)
    x_min_val -= min(path_xs)
    x_max_val -= min(path_xs)

    # the maximum distance the sand pile can extend is determined by the 
    # angle of repose which is 1:1. Take whichever is greater, starting from the
    # starting point of the left and right most paths
    distance_left = max(height,
                        x_min_val + (height - path_ys[x_min_index]))
    distance_right = max(height,
                         x_max_val + (height - path_ys[x_max_index])) + 1

    # determine how much space needs to be added to the domain
    add_left = abs(distance_left - start_ind[1])
    add_right = abs(distance_right - (domain.shape[1] - start_ind[1]))
    new_width = add_left + domain.shape[1] + add_right

    # create the arrays to append
    left_array = np.empty(shape=(domain.shape[0], add_left), dtype=str)
    right_array = np.empty(shape=(domain.shape[0], add_right), dtype=str)
    bottom_array = np.empty(shape=(2, new_width), dtype=str)

    # populate the new domain parts
    left_array[:, :] = "."
    right_array[:, :] = "."
    bottom_array[0, :] = "."
    bottom_array[1, :] = "#"

    # reindex wthe starting point given the new domain
    start_ind = (start_ind[0], start_ind[1] + add_left)

    # create the new domain
    new_domain = np.append(np.append(np.append(left_array, domain, axis=1), right_array, axis=1), bottom_array, axis=0)

    return (new_domain, start_ind)


def fill_domain(domain: np.ndarray, start_ind: tuple[int, int]) -> tuple[np.ndarray, int]:
    ''' Iteratively fill up the cavern, return the final state of the domain
    and the grains of sand'''
    flag = True
    grain_ind = start_ind

    while flag:
        updated_index = check_move(domain, grain_ind)
        if domain[grain_ind] == "o":
            # the sand has filled up the domain, end the simulation
            flag = False
            continue
        if updated_index == "next":
            # the grian has come to rest, set the point as being filled
            # and begin again with the next grain at the starting point
            domain[grain_ind] = "o"
            grain_ind = start_ind
            continue
        if not updated_index:
            # the gain has fallen off the domain, end the simulation
            flag = False
            continue
        # if none of the above the grain continues to fall
        grain_ind = updated_index

    # return the domain and the total number of grains
    return domain, sum(sum(domain == "o"))


if __name__ == "__main__":

    # set-up
    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        data = f.read().split('\n')
    paths_x, paths_y = extract_paths(data)

    # part_1
    domain, start_ind = make_domain_part_1(path_xs=paths_x, path_ys=paths_y)
    domain, sand_ind = fill_domain(domain, start_ind)
    print("The solution to part 1 is", sand_ind)

    # part_2
    part_2_domain, start_ind = make_domain_part_2(path_xs=paths_x, path_ys=paths_y)
    part_2_domain, sand_ind = fill_domain(part_2_domain, start_ind)
    print("The solution to part 2 is", sand_ind)
