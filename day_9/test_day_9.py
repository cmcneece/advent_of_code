from .day_9 import part_1, part_2, extract_instructions, Instruction
import numpy as np


def setup_tests(part: int) -> tuple[list[Instruction], list[np.array]]:
    ''' Accept the part of the challenges to test,
    returns the instructions and rope'''
    print(part)
    if part == 1:
        input_path = 'part_1_test_input.txt'
        rope_length = 2
    elif part == 2:
        input_path = 'part_2_test_input.txt'
        rope_length = 10
    else:
        print('no')
        raise ValueError("Unknown part to test")

    rope = [np.array([[0], [0]]) for _ in range(rope_length)]
    with open(input_path, 'r') as f:
        data = f.read().splitlines()

    instructions = extract_instructions(data)
    return (instructions, rope)


def test_part_1() -> bool:
    ''' Tests part 1 '''
    instructions, part_1_rope = setup_tests(part=1)
    part_1_solution = part_1(instructions, part_1_rope)
    true_answer = 13
    assert true_answer == part_1_solution


def test_part_2() -> bool:
    ''' Tests part 2 '''
    instructions, part_2_rope = setup_tests(part=2)
    part_2_solution = part_2(instructions, part_2_rope)
    true_answer = 36
    assert true_answer == part_2_solution
