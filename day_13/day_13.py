import functools
import pathlib
import os

DIR_PATH = pathlib.Path(__file__).parent.resolve()


def compare(left: int, right: int) -> int:
    """Compare the deepest part of signal lists, return 1, 0, -1 depending on values"""
    if left < right:
        return 1
    elif left > right:
        return -1
    else:
        return 0


def compare_packets(left: list[int, list], right: list[int, list]) -> int:
    """Compare packet pairs"""
    match left, right:
        case int(), int():
            return compare(left, right)
        case int(), list():
            return compare_packets([left], right)
        case list(), int():
            return compare_packets(left, [right])
        case list(), list():
            for l, r in zip(left, right):
                result = compare_packets(l, r)
                if result != 0:
                    return result
            return compare_packets(len(left), len(right))


def get_pairs(data: str) -> tuple[list]:
    """Pulls out the packet pairs form the input str"""
    left_entries = [eval(line) for line in data[::3]]
    right_entries = [eval(line) for line in data[1::3]]
    return (left_entries, right_entries)


def flatten(pairs: tuple[list[int, list]]) -> list:
    """Turn the tuple of packets into a flat list for sorting"""
    flattened = []
    for left, right in zip(*pairs):
        flattened.append(left)
        flattened.append(right)

    return flattened


def part_1(pairs: tuple[list[list, int]]) -> int:
    """Execute part 1 of puzzle"""
    sum_of_indices = 0
    lefts, rights = pairs
    for index, (left, right) in enumerate(zip(lefts, rights)):
        if compare_packets(left, right) == 1:
            sum_of_indices += index + 1
    return sum_of_indices


def part_2(pairs: tuple[list[list, int]]) -> int:
    """Execute part 2 of puzzle"""
    dividers = [[[2]], [[6]]]
    pairs[0].append(dividers[0])
    pairs[1].append(dividers[1])

    flattened = flatten(pairs)

    result = sorted(flattened, key=functools.cmp_to_key(compare_packets))
    result = result[::-1]

    ind_1 = result.index(dividers[0])+1
    ind_2 = result.index(dividers[1])+1
    return ind_1 * ind_2


if __name__ == "__main__":

    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        data = f.read().split('\n')

    pairs = get_pairs(data)
    part_1_answer = part_1(pairs)
    part_1_msg = f"The sum of the indices of pairs that are in the correct\
        order is {part_1_answer}"
    print(part_1_msg)

    part_2_answer = part_2(pairs)
    part_2_msg = f"The decoder key is {part_2_answer}"
    print(part_2_msg)
