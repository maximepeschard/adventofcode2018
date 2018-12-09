from typing import Sequence


def final_frequency(changes: Sequence[int]) -> int:
    """Compute the resulting frequency after a list of changes"""
    return sum(changes)


def first_frequency_twice(changes: Sequence[int]) -> int:
    """
    Compute the first frequency reached twice when repeating
    a list of changes
    """
    frequency = 0
    counts = {frequency: 1}
    found = False
    while not found:
        for change in changes:
            frequency += change
            count = counts.get(frequency, 0) + 1
            if count == 2:
                found = True
                break
            counts[frequency] = count
    return frequency
