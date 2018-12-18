from typing import Sequence


def score_after(rounds: int, recipes: int, initial: Sequence[int]) -> str:
    """
    Find the scores of the ten recipes immediately after a number of
    recipes (or `rounds`).
    """
    scores = list(initial)
    elves_positions = list(range(len(initial)))
    min_length = rounds + recipes
    while len(scores) < min_length:
        score_sum = sum(scores[i] for i in elves_positions)
        for digit in (int(c) for c in str(score_sum)):
            scores.append(digit)
        elves_positions = [(i + 1 + scores[i]) % len(scores) for i in elves_positions]

    return "".join(str(n) for n in scores[rounds:min_length])


def recipes_before(sequence: str, initial: Sequence[int]) -> int:
    """
    Compute the number of recipes appearing on the scoreboard to the left of
    a score sequence.
    """
    scores = list(initial)
    elves_positions = list(range(len(initial)))
    target = [int(c) for c in sequence]
    position_in_target = 0
    while position_in_target < len(target):
        score_sum = sum(scores[i] for i in elves_positions)
        for digit in (int(c) for c in str(score_sum)):
            scores.append(digit)
            if digit == target[position_in_target]:
                position_in_target += 1
            else:
                position_in_target = int(digit == target[0])
            if position_in_target == len(target):
                break
        elves_positions = [(i + 1 + scores[i]) % len(scores) for i in elves_positions]

    return len(scores) - len(target)
