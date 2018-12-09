from typing import List, Set
import string
import sys


def react(unit_left: str, unit_right: str) -> bool:
    """Find if two adjacent units react"""
    return unit_left != unit_right and unit_left.lower() == unit_right.lower()


def reduction(polymer: str, ignore: Set[str] = set()) -> int:
    """
    Compute the number of units contained in a polymer after applying
    all possible reactions.
    """
    scanned: List[str] = []
    polymer_index = 0
    while polymer_index < len(polymer):
        right = polymer[polymer_index]
        if right in ignore:
            polymer_index += 1
            continue
        try:
            left = scanned.pop()
        except IndexError:
            # nothing scanned yet
            scanned.append(right)
        else:
            if not react(left, right):
                scanned.append(left)
                scanned.append(right)
        polymer_index += 1
    return len(scanned)


def best_reduction(polymer: str) -> int:
    """
    Compute the length of the shortest polymer produced by removing
    exactly one unit type
    """
    best = sys.maxsize
    for unit_type in string.ascii_lowercase:
        length = reduction(polymer, ignore={unit_type, unit_type.upper()})
        if length < best:
            best = length
    return best
