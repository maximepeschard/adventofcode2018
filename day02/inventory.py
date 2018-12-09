from typing import Tuple, Dict, Sequence, List
from functools import reduce
import operator


def sum_pairs(t: Tuple[int, int], u: Tuple[int, int]) -> Tuple[int, int]:
    """Compute the component-wise sum of two pairs"""
    return t[0] + u[0], t[1] + u[1]


def classify_candidate(box_id: str) -> Tuple[int, int]:
    """
    Compute whether a box id contains exactly two of any letter,
    exactly three of any letter or both.

    Examples:

        >>> classify_candidate("aabcde")
        (1, 0)
        >>> classify_candidate("aaabcd")
        (0, 1)
        >>> classify_candidate("aaabcc")
        (1, 1)
    """
    counts: Dict[str, int] = {}
    double_letters, triple_letters = 0, 0
    for letter in box_id:
        count = counts.get(letter, 0) + 1
        counts[letter] = count
        if count == 2:
            double_letters += 1
        elif count == 3:
            triple_letters += 1
            double_letters -= 1
    return int(double_letters > 0), int(triple_letters > 0)


def checksum(box_ids: Sequence[str]) -> int:
    """Compute the checksum of a list of box ids"""
    classes = (classify_candidate(box_id) for box_id in box_ids)
    counts = reduce(sum_pairs, classes, (0, 0))
    return reduce(operator.mul, counts, 1)


def common_letters_prototype(box_ids: Sequence[str]) -> str:
    """Get common letters between the two correct ids of a list of box ids

    To reduce complexity, we first sort the list of ids alphabetically.
    Then, since the two correct ids only differ by a letter, they must be
    next to each other in the sorted list.
    """
    sorted_ids = sorted(box_ids)
    index = 0
    common_letters: List[str] = []
    for index in range(1, len(sorted_ids)):
        current_id = sorted_ids[index]
        previous_id = sorted_ids[index - 1]

        # For a fixed pair of ids, we count letters by which they differ
        common_letters = []
        diffs = 0
        for letter_index in range(len(current_id)):
            if current_id[letter_index] != previous_id[letter_index]:
                diffs += 1
            else:
                common_letters.append(current_id[letter_index])
            if diffs > 1:
                # Correct ids only differ by 1 letter, no need to count further
                break
        if diffs == 1:
            break
    return "".join(common_letters)
