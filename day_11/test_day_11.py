from .day_11 import execute_rounds, parse_input, Monkey


def set_up() -> tuple[list[Monkey], int]:
    ''' sets up the input tests'''
    INPUT_PATH = 'test_input.txt'

    monkeys, supermodulo = parse_input(INPUT_PATH)
    return monkeys, supermodulo


def test_part_1():
    ''' Tests part 1'''
    part_1_true_answer = 10605
    monkeys, supermodulo = set_up()
    part_1_solution = execute_rounds(monkeys=monkeys, rounds=20,
                                     part=1, supermodulo=supermodulo)

    assert part_1_solution == part_1_true_answer


def test_part_2():
    ''' Tests part 2'''
    part_2_true_answer = 2713310158
    monkeys, supermodulo = set_up()
    part_2_solution = execute_rounds(monkeys=monkeys, rounds=10000,
                                     part=2, supermodulo=supermodulo)

    assert part_2_solution == part_2_true_answer
