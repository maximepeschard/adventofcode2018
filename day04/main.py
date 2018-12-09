from common import root
from .guards import parse_record, guard_stats, strategy_1, strategy_2


def run() -> None:
    with open(root / "day04" / "input.txt") as fin:
        records = [parse_record(line.strip()) for line in fin]
        stats = guard_stats(records)
        result_part_1 = strategy_1(stats)
        print(result_part_1)
        result_part_2 = strategy_2(stats)
        print(result_part_2)
