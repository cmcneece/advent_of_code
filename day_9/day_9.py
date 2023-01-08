from collections import namedtuple
import numpy as np

# translation of input direction into a movement vector
DIRECTION_MAPPING = {'R': np.array([[1], [0]]),
                     'L': np.array([[-1], [0]]),
                     'U': np.array([[0], [1]]),
                     'D': np.array([[0], [-1]])}

# easy storage of input instructions
Instruction = namedtuple('Instruction', ['direction', 'distance'])


def extract_instructions(data: str) -> dict[int, namedtuple]:
    ''' Accepts the input string and returns the instruction set'''

    instructions = []
    for row in data:
        direction, distance = row.split(' ')
        instruction = Instruction(direction=direction, distance=int(distance))
        instructions.append(instruction)

    return instructions


def update_position(t_pos: np.array, h_pos: np.array) -> np.array:
    ''' Accepts the leading and trailing knot, returns the updated
    trailing knot position '''
    move = np.array([[0], [0]])

    # distance vector
    delta = h_pos - t_pos

    # how to move to catch up
    if np.sum(np.abs(delta)) >= 3:
        # move diagonally
        move[0] = np.sign(delta[0])
        move[1] = np.sign(delta[1])
    else:
        move[0] = 0 if np.abs(delta[0]) < 2 else np.sign(delta[0])
        move[1] = 0 if np.abs(delta[1]) < 2 else np.sign(delta[1])

    # update t position
    t_pos = t_pos + move

    return t_pos


def num_unique_positions(positions: list) -> int:
    ''' Accepts the list of knot positions, returns the number of
    unique positions the knot has occupied'''
    uniques = set([tuple(sum(position.tolist(), []))
                  for position in positions])

    return len(uniques)


def part_1(instructions: list, rope: list) -> int:
    ''' Accepts the instruction list and rope, returns the answer to part 1'''

    h_position = rope[0]
    t_position = rope[1]

    h_positions = [h_position]
    t_positions = [t_position]

    for instruction in instructions:
        for _ in range(instruction.distance):
            # update h position
            h_position = h_position + DIRECTION_MAPPING[instruction.direction]
            t_position = update_position(t_position, h_position)

            h_positions.append(h_position)
            t_positions.append(t_position)

    return num_unique_positions(t_positions)


def part_2(instructions: list, rope: list) -> int:
    ''' Accepts the instruction list and rope, returns the answer to part 2'''

    h_positions = [rope[0]]
    t_positions = [rope[-1]]

    for instruction in instructions:
        for _ in range(instruction.distance):

            # update h position
            rope[0] = rope[0] + DIRECTION_MAPPING[instruction.direction]

            # propogate the movement down the rope
            for i in range(1, len(rope)):

                rope[i] = update_position(rope[i], rope[i-1])

                h_positions.append(rope[0])
                t_positions.append(rope[-1])

    return num_unique_positions(t_positions)


if __name__ == "__main__":

    INPUT_PATH = 'input.txt'

    with open(INPUT_PATH, 'r') as f:
        data = f.read().splitlines()

    instructions = extract_instructions(data)

    # part 1
    part_1_rope = [np.array([[0], [0]]) for _ in range(2)]
    part_1_solution = part_1(instructions, part_1_rope)
    msg = "In part 1 the tail occupies {num_unqiue} unique positions"
    print(msg.format(num_unqiue=part_1_solution))

    # part 2
    part_2_rope = [np.array([[0], [0]]) for _ in range(10)]
    part_2_solution = part_2(instructions, part_2_rope)
    msg = "In part 2 the tail occupies {num_unqiue} unique positions"
    print(msg.format(num_unqiue=part_2_solution))
