from common import root
from .calibration import final_frequency, first_frequency_twice


def run() -> None:
    with open(root / "day01" / "input.txt") as fin:
        changes = [int(line) for line in fin]
        result_part_1 = final_frequency(changes)
        print(result_part_1)
        result_part_2 = first_frequency_twice(changes)
        print(result_part_2)
