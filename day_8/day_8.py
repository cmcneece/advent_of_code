import numpy as np
import pathlib
import os


DIR_PATH = pathlib.Path(__file__).parent.resolve()


def get_forest_data(input_path: str) -> np.array:
    ''' Takes the forest data input path and returns the data as an array'''
    with open(input_path, 'r') as f:
        data = f.read().splitlines()

    full_data = []
    for row in data:
        full_data.append([*row])

    return np.array(full_data, dtype=int)


def part_1(forest_data: np.array) -> int:
    ''' Takes the forest data and returns the answer to part 1'''

    count = 0
    for (row_ind, col_ind), x in np.ndenumerate(forest_data):
        # pull out the data for each direction
        west = forest_data[row_ind, :col_ind]
        east = forest_data[row_ind, col_ind+1:]
        north = forest_data[:row_ind, col_ind]
        south = forest_data[row_ind+1:, col_ind]

        # see if the view to the boundary is blocked
        look_west = not any(west >= x)
        look_east = not any(east >= x)
        look_north = not any(north >= x)
        look_south = not any(south >= x)

        if look_west | look_east | look_north | look_south:
            count += 1

    return count


def view_score(view_array: np.array, direction: str = None) -> int:
    ''' Takes a view array and return how many trees can be seen '''
    ind = 0
    score = 0
    if direction == 'flip':
        view_array = np.flip(view_array)

    if len(view_array) == 0:
        # at the boundary, no trees to see
        return 0

    # go until we dont see any trees or reach the boundary
    while view_array[ind]:
        ind += 1
        if ind >= len(view_array):
            break

    if ind != len(view_array):
        # count the view blocking tree
        score = ind + 1
    else:
        # we can see all the way to the boundary
        score = ind

    return score


def part_2(forest_data: np.array) -> int:
    ''' Takes the forest data, and returns the answer to part 2 '''

    scenic_score = np.empty_like(forest_data)

    for (row_ind, col_ind), x in np.ndenumerate(forest_data):
        # pull out the trees in each direction
        west = forest_data[row_ind, :col_ind]
        east = forest_data[row_ind, col_ind+1:]
        north = forest_data[:row_ind, col_ind]
        south = forest_data[row_ind+1:, col_ind]

        # mark the trees that are lower than the current tree
        look_west = west < x
        look_east = east < x
        look_north = north < x
        look_south = south < x

        # count how many trees can be seen in each direction
        west_score = view_score(look_west, 'flip')
        east_score = view_score(look_east)
        north_score = view_score(look_north, 'flip')
        south_score = view_score(look_south)

        # the scenic score is the product of all the scores
        scenic_score[row_ind, col_ind] = west_score * east_score * north_score * south_score

    return np.amax(scenic_score)


if __name__ == "__main__":
    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    forest_data = get_forest_data(INPUT_PATH)

    part_1_answer = part_1(forest_data)
    part_1_msg = '{answer} trees are visible from outside the grid.'
    print(part_1_msg.format(answer=part_1_answer))

    part_2_answer = part_2(forest_data)
    part_2_msg = '{answer} is the highest scenic score possible.'
    print(part_2_msg.format(answer=part_2_answer))
