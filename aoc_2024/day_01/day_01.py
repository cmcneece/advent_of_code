import collections
import pathlib
import os

DIR_PATH = pathlib.Path(__file__).parent.resolve()


def clean_and_sort(data):
    left, right = [], []

    for item in data:
        left_item, right_item = item.split()
        left.append(int(left_item))
        right.append(int(right_item))

    left.sort()
    right.sort()
    return left, right


def part_1(data, verbose=True):

    left, right = clean_and_sort(data)

    deltas = [abs(left_item - right_item) for left_item, right_item
              in zip(left, right)]

    part_1_answer = sum(deltas)

    if verbose:
        print("--- Part 1 ---")
        part_1_msg = f"The total distance between your lists is: {part_1_answer}"
        print(part_1_msg)
    return part_1_answer


def part_2(data, verbose=True):
    left, right = clean_and_sort(data)
    right_count = collections.Counter(right)

    sim_scores = []
    for item in left:
        sim_scores.append(item * right_count[item])

    part_2_answer = sum(sim_scores)

    if verbose:
        print("--- Part 2 ---\r")
        part_2_msg = f"The similarity score is: {part_2_answer}"
        print(part_2_msg)

    return part_2_answer


if __name__ == "__main__":
    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()

    # Part 1
    part_1_answer = part_1(data)

    # Part 2
    part_2_answer = part_2(data)
