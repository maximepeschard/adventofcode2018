from common import root
from .steps import parse_requirement, complete


def run() -> None:
    with open(root / "day07" / "input.txt") as fin:
        requirements = [parse_requirement(line.strip()) for line in fin]
        result_part_1, _ = complete(requirements, 1, 0)
        print(result_part_1)
        _, result_part_2 = complete(requirements, 5, 60)
        print(result_part_2)
