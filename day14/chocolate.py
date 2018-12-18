from typing import Sequence


def score_after(rounds: int, recipes: int, initial: Sequence[int]) -> str:
    scores = list(initial)
    elves_position = list(range(len(initial)))
    min_length = rounds + recipes
    while len(scores) < min_length:
        score_sum = sum(scores[i] for i in elves_position)
        for digit in (int(c) for c in str(score_sum)):
            scores.append(digit)
        elves_position = [(i + 1 + scores[i]) % len(scores) for i in elves_position]

    return "".join(str(n) for n in scores[rounds:min_length])


def recipes_before(sequence: str, initial: Sequence[int]) -> int:
    scores = list(initial)
    elves_position = list(range(len(initial)))
    target = [int(c) for c in sequence]
    pos_in_target = 0
    while pos_in_target < len(target):
        score_sum = sum(scores[i] for i in elves_position)
        for digit in (int(c) for c in str(score_sum)):
            scores.append(digit)
            if digit == target[pos_in_target]:
                pos_in_target += 1
            else:
                pos_in_target = int(digit == target[0])
            if pos_in_target == len(target):
                break
        elves_position = [(i + 1 + scores[i]) % len(scores) for i in elves_position]

    return len(scores) - len(target)
