import collections
import pathlib
import os

DIR_PATH = pathlib.Path(__file__).parent.resolve()


def get_reports(data):
    reports = []
    for report in data:
        levels = [int(level) for level in report]
        reports.append(levels)
    return reports

def part_1(reports, verbose=True):

    safe_count = 0

    for report in reports:
        deltas = report[0:] - report[1:]
        print(deltas)


    # if verbose:
    #     print("--- Part 1 ---")
    #     part_1_msg = f"The number of safe reports is: \
    #       {part_1_answer}"
    #     print(part_1_msg)
    # return part_1_answer


def part_2(data, verbose=True):
    left, right = get_reports(data)
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
    INPUT_FILE = 'test_input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)
    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()

    reports = get_reports(data)
    # Part 1
    part_1_answer = part_1(reports, verbose=False)

    # Part 2
    # part_2_answer = part_2(data)
