from common import root
from .inventory import checksum, common_letters_prototype


def run() -> None:
    with open(root / "day02" / "input.txt") as fin:
        box_ids = [line.strip() for line in fin]
        result_part_1 = checksum(box_ids)
        print(result_part_1)
        result_part_2 = common_letters_prototype(box_ids)
        print(result_part_2)
