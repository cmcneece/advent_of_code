INTERESTING_CYCLES = [20, 60, 100, 140, 180, 220]


def part_1(instructions):
    cycle = 1
    register = 1
    register_values = {cycle: (register, cycle*register)}

    for instruction in instructions:
        command = instruction[0]

        if command == 'noop':
            cycle += 1
            register_values[cycle] = (register, cycle*register)
        elif command == 'addx':
            cycle += 1
            register_values[cycle] = (register, cycle*register)

            cycle += 1
            register += int(instruction[1])
            register_values[cycle] = (register, cycle*register)

    signal_strength_sum = 0
    for cycle in INTERESTING_CYCLES:
        signal_strength = register_values[cycle][1]
        signal_strength_sum += signal_strength

    return signal_strength_sum


if __name__ == "__main__":
    INPUT_PATH = 'input.txt'

    with open(INPUT_PATH, 'r') as f:
        instructions = [line.strip().split() for line in f.readlines()]

    part_1_answer = part_1(instructions)
    MSG = 'The sum of signal strengths for cycles {interesting_cycle} is {signal_sum}'
    print(MSG.format(interesting_cycle=INTERESTING_CYCLES, signal_sum=part_1_answer))
