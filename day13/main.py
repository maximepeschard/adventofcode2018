from common import root
from .carts import parse_map, first_crash_location, last_cart_location


def run() -> None:
    with open(root / "day13" / "input.txt") as fin:
        tracks, carts = parse_map(fin.readlines())
    result_part_1 = first_crash_location(tracks, carts)
    print(result_part_1)
    result_part_2 = last_cart_location(tracks, carts)
    print(result_part_2)
