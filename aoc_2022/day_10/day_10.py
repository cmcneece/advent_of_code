from collections import namedtuple
import pandas as pd
import numpy as np
import pathlib
import os


DIR_PATH = pathlib.Path(__file__).parent.resolve()

INTERESTING_CYCLES = [20, 60, 100, 140, 180, 220]

Register = namedtuple("Register", ["register", "signal_strength"])


def pretty_print(input_array: np.ndarray) -> None:
    ''' Prints the screen in a pretty way'''
    A = pd.DataFrame(input_array)
    A.columns = ['']*A.shape[1]
    print(A.to_string(index=False))


def execute_instructions(instructions: list[str]) -> dict[int, Register]:
    ''' Takes the instruction input and returns the cycle, register, 
    and signal strength'''
    cycle = 1
    register = 1
    register_values = {cycle: Register(register=register,
                                       signal_strength=cycle*register)}

    for instruction in instructions:
        command = instruction[0]

        # both noop and addx take at least one cycle where nothing is done
        cycle += 1
        register_values[cycle] = Register(register=register,
                                          signal_strength=cycle*register)

        if command == 'addx':
            # addx adds to the register and takes two cycles to execute
            cycle += 1
            register += int(instruction[1])
            register_values[cycle] = Register(register=register,
                                              signal_strength=cycle*register)

    return register_values


def get_signal_strength(register_values: dict[int, Register]) -> int:
    ''' Calculates the sum of signal strength for the cycles of interest'''
    signal_strength_sum = 0
    for cycle in INTERESTING_CYCLES:
        signal_strength_sum += register_values[cycle].signal_strength

    return signal_strength_sum


def part_2(register_values: dict[int, Register], to_print: bool) -> np.ndarray:
    ''' Takes the register values and returns the screen output'''
    if to_print is None:
        to_print = False
    screen = np.ndarray(shape=(6, 40), dtype=object)
    num_el = screen.shape[0]*screen.shape[1]
    for i in range(num_el):
        cycle = i+1
        sprite_position = register_values[cycle].register
        x, y = np.unravel_index(i, shape=screen.shape)
        sprite_pixels = [sprite_position-1, sprite_position, sprite_position+1]
        if i - x*screen.shape[1] in sprite_pixels:
            screen[x, y] = '#'
        else:
            screen[x, y] = '.'
    if to_print:
        pretty_print(screen)

    return screen


if __name__ == "__main__":
    INPUT_FILE = 'input.txt'
    INPUT_PATH = os.path.join(DIR_PATH, INPUT_FILE)

    with open(INPUT_PATH, 'r') as f:
        instructions = [line.strip().split() for line in f.readlines()]

    register_values = execute_instructions(instructions)
    part_1_answer = get_signal_strength(register_values)
    MSG = 'The sum of signal strengths for cycles {interesting_cycle} is {signal_sum}'
    print(MSG.format(interesting_cycle=INTERESTING_CYCLES,
                     signal_sum=part_1_answer))

    part_2(register_values, to_print=True)
