from dataclasses import dataclass
from math import floor, prod
import copy


@dataclass
class Monkey:
    """ Monkey item."""
    id: int
    items: list[int]
    operation: tuple[callable, int]
    test_factor: int
    true_monkey: int
    false_monkey: int
    items_inspected: int = 0

    def test_function(self, item: int) -> bool:
        '''Evaluates if an item passes the test'''
        return (item % self.test_factor) == 0

    def inspect(self, monkeys: dict[int, Monkey], part: int, supermodulo: int) -> dict[int, Monkey]:
        '''Inspect items and toss them to othe monkeys'''
        for item in self.items:
            old = item
            # adjust anxiety levels
            new = eval(self.operation)
            if part == 1:
                new = floor(new / 3)
            elif part == 2:
                new %= supermodulo

            destination_monkey = self.true_monkey \
                if self.test_function(new) else self.false_monkey
            monkeys[destination_monkey].items.append(new)
            self.items_inspected += 1

        self.items = []

        return monkeys


def parse_input(input_path: str) -> tuple[dict[int, Monkey], int]:
    ''' Parses the input text, returns the monkeys and supermodulo'''
    with open(input_path, 'r') as f:
        data = f.readlines()

    block_start = range(0, len(data), 7)
    block_stop = range(6, len(data)+1, 7)

    blocks = []
    for start, stop in zip(block_start, block_stop):
        blocks.append(data[start:stop])

    monkeys = {}
    supermodulo = 1
    for block in blocks:
        for j, _ in enumerate(block):

            # remove all spaces and \n
            line = block[j].strip()

            if j == 0:
                # monkey id
                line = line.strip(":")
                id = int(line.split()[1])
            elif j == 1:
                # current items
                items_text = line.split(":")[1].split(",")
                items = []
                for entry in items_text:
                    items.append(int(entry.strip()))
            elif j == 2:
                # operation
                operation = line.split(":")[1].strip(",").replace(" ", "").replace("new=", "")
            elif j == 3:
                test_factor = int(line.replace("Test: divisible by", ""))
                supermodulo *= test_factor
            elif j == 4:
                true_monkey = int(line.replace("If true: throw to monkey ", ""))
            elif j == 5:
                false_monkey = int(line.replace("If false: throw to monkey ", ""))

        monkey = Monkey(id=id, items=items, operation=operation, test_factor=test_factor,
                        true_monkey=true_monkey, false_monkey=false_monkey)

        monkeys[id] = monkey

    return monkeys, supermodulo


def execute_rounds(monkeys: dict[int, Monkey], rounds: int, part: int, supermodulo: int):
    ''' Executes rounds of monkey inspection and tossing'''
    for _ in range(rounds):
        for id in range(len(monkeys)):
            monkeys = monkeys[id].inspect(monkeys=monkeys, part=part,
                                          supermodulo=supermodulo)

    items_inspected = []
    for _, monkey in monkeys.items():
        items_inspected.append(monkey.items_inspected)

    items_inspected.sort()

    monkey_business = prod(items_inspected[-2:])
    return monkey_business


if __name__ == "__main__":
    INPUT_PATH = 'input.txt'
    MSG = "Part {part} solution is {solution}"

    monkeys, supermodulo = parse_input(INPUT_PATH)
    part_1_monkeys = copy.deepcopy(monkeys)
    part_2_monkeys = copy.deepcopy(monkeys)

    part_1_solution = execute_rounds(monkeys=part_1_monkeys, rounds=20, part=1,
                                     supermodulo=supermodulo)
    print(MSG.format(part=1, solution=part_1_solution))

    part_2_solution = execute_rounds(monkeys=part_2_monkeys, rounds=10000, part=2,
                                     supermodulo=supermodulo)
    print(MSG.format(part=2, solution=part_2_solution))
