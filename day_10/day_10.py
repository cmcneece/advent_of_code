from collections import namedtuple
import pandas as pd
import numpy as np

INTERESTING_CYCLES = [20, 60, 100, 140, 180, 220]

Register = namedtuple("Register", ["register", "signal_strength"])


def pretty_print(input_array: np.ndarray) -> None:
    A = pd.DataFrame(input_array)
    A.columns = ['']*A.shape[1]
    print(A.to_string(index=False))


def execute_instructions(instructions):
    cycle = 1
    register = 1
    register_values = {cycle: Register(register=register, signal_strength=cycle*register)}

    for instruction in instructions:
        command = instruction[0]

        if command == 'noop':
            cycle += 1
            register_values[cycle] = Register(register=register,
                                              signal_strength=cycle*register)
        elif command == 'addx':
            cycle += 1
            register_values[cycle] = Register(register=register,
                                              signal_strength=cycle*register)

            cycle += 1
            register += int(instruction[1])
            register_values[cycle] = Register(register=register,
                                              signal_strength=cycle*register)

    return register_values


def get_signal_strength(register_values):
    signal_strength_sum = 0
    for cycle in INTERESTING_CYCLES:
        signal_strength_sum += register_values[cycle].signal_strength

    return signal_strength_sum


def part_2(register_values, to_print: bool):
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
    INPUT_PATH = 'input.txt'

    with open(INPUT_PATH, 'r') as f:
        instructions = [line.strip().split() for line in f.readlines()]

    register_values = execute_instructions(instructions)
    part_1_answer = get_signal_strength(register_values)
    MSG = 'The sum of signal strengths for cycles {interesting_cycle} is {signal_sum}'
    print(MSG.format(interesting_cycle=INTERESTING_CYCLES, signal_sum=part_1_answer))

    part_2(register_values, to_print=True)
