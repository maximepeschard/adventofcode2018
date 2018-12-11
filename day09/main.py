from common import root
from .marbles import parse_game_setup, highest_score


def run() -> None:
    with open(root / "day09" / "input.txt") as fin:
        players, last_marble = parse_game_setup(fin.read())
        result_part_1 = highest_score(players, last_marble)
        print(result_part_1)
        result_part_2 = highest_score(players, last_marble * 100)
        print(result_part_2)
