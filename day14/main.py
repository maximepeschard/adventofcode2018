from .chocolate import score_after, recipes_before


def run() -> None:
    initial_scores = (3, 7)
    puzzle_input = 894501
    result_part_1 = score_after(puzzle_input, 10, initial_scores)
    print(result_part_1)
    result_part_2 = recipes_before(str(puzzle_input), initial_scores)
    print(result_part_2)
