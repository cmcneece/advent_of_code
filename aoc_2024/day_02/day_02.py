import pathlib
import os

DIR_PATH = pathlib.Path(__file__).parent.resolve()


def get_reports(data):
    reports = []
    for report in data:
        levels = [int(level) for level in report.split()]
        reports.append(levels)
    return reports


def int_sign(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0


def get_deltas(report):
    deltas = [report[i+1] - report[i] for i in range(0, len(report)-1)]
    return deltas


def is_safe(report):
    """Check if a report has unsafe deltas."""
    deltas = get_deltas(report)

    delta_signs = list(map(int_sign, deltas))
    if abs(sum(delta_signs)) != len(report)-1:
        return False

    for delta in deltas:
        if not (1 <= abs(delta) <= 3):
            return False

    return True


def part_1(reports):

    safe_count = 0

    for report in reports:
        # Check if the report is unsafe
        if is_safe(report):
            safe_count += 1

    return safe_count


def part_2(reports):

    safe_count = 0

    for report in reports:
        if is_safe(report):
            safe_count += 1  # Already safe, no need for modification
            continue

        # Try removing each level to see if it can make the report safe
        for i in range(len(report)):
            modified_report = report[:i] + report[i + 1:]
            if is_safe(modified_report):
                safe_count += 1
                break  # No need to check further removals for this report

    return safe_count


if __name__ == "__main__":

    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()

    reports = get_reports(data)

    # Part 1
    part_1_answer = part_1(reports)
    part_1_msg = f"For Part 1 there are {part_1_answer} safe reports."
    print(part_1_msg)

    # Part 2
    part_2_answer = part_2(reports)
    part_2_msg = f"For Part 2 there are {part_2_answer} safe reports."
    print(part_2_msg)
