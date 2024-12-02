from .day_10 import get_signal_strength, part_2, execute_instructions
import numpy as np
import pathlib
import os


DIR_PATH = pathlib.Path(__file__).parent.resolve()

INPUT_FILE = 'test_input.txt'
INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)


def set_up():
    ''' Loads the input and returns the register values'''
    with open(INPUT_PATH, 'r') as f:
        instructions = [line.strip().split() for line in f.readlines()]
    register_values = execute_instructions(instructions)

    return register_values


def test_part_1():
    ''' Tests part 1 of the puzzle'''
    part_1_true_answer = 13140
    register_values = set_up()
    part_1_answer = get_signal_strength(register_values)

    assert part_1_true_answer == part_1_answer


def test_part_2():
    ''' Tests part 2 of the puzzle'''
    answer_text = "##..##..##..##..##..##..##..##..##..##..\
###...###...###...###...###...###...###.\
####....####....####....####....####....\
#####.....#####.....#####.....#####.....\
######......######......######......####\
#######.......#######.......#######....."
    print(len(answer_text))

    answer_screen = np.ndarray(shape=(6, 40), dtype=object)
    for i, val in enumerate(answer_text):
        x, y = np.unravel_index(i, shape=answer_screen.shape)
        answer_screen[x, y] = val

    register_values = set_up()
    screen = part_2(register_values, to_print=False)
    comparison = answer_screen == screen
    assert comparison.all()
