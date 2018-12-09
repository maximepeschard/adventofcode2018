from common import root
from .license import make_tree, total_metadata, value


def run() -> None:
    with open(root / "day08" / "input.txt") as fin:
        values = [int(n) for n in fin.read().split()]
        tree = make_tree(values)
        result_part_1 = total_metadata(tree)
        print(result_part_1)
        result_part_2 = value(tree)
        print(result_part_2)
