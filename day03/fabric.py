from typing import NamedTuple, Optional, Sequence, Tuple, Set, List
import re


class Claim(NamedTuple):
    id: int
    left: int
    top: int
    width: int
    height: int


def parse_claim(description: str) -> Optional[Claim]:
    """Parse a claim textual description"""
    match = re.match(
        r"#(?P<id>\d+)\s+@\s+(?P<left>\d+),(?P<top>\d+):\s+(?P<width>\d+)x(?P<height>\d+)",
        description,
    )
    if not match:
        raise Exception("invalid claim")
    parsed = match.groupdict()
    return Claim(
        int(parsed["id"]),
        int(parsed["left"]),
        int(parsed["top"]),
        int(parsed["width"]),
        int(parsed["height"]),
    )


def overlapping(claims: Sequence[Claim], min_claims: int) -> Tuple[int, Set[int]]:
    """
    Compute how many square inches of fabric are within two or more claims and
    the ID of the only claim that doesn't overlap.
    """

    # Since the grid size is not known in advance, we go through the list of claims
    # to find the maximum positions.
    width, height = 0, 0
    for claim in claims:
        if claim.left + claim.width > width:
            width = claim.left + claim.width + 1
        if claim.top + claim.height > height:
            height = claim.top + claim.height + 1

    # A set is associated to each square of the grid and each claim is applied
    # by adding its ID to the sets of the squares it covers. This allows us to
    # determine the number of claims made on a square, and to keep track of
    # claims not overlapping any other claim.
    grid: List[List[Set[int]]] = [[set() for _ in range(width)] for _ in range(height)]
    overlap = 0
    not_overlapping_claims = set()
    for claim in claims:
        did_overlap = False
        overlapped = set()
        for i in range(claim.top, claim.top + claim.height):
            for j in range(claim.left, claim.left + claim.width):
                grid[i][j].add(claim.id)
                if len(grid[i][j]) == min_claims:
                    overlap += 1
                if len(grid[i][j]) >= min_claims:
                    did_overlap = True
                    overlapped.update(grid[i][j])
        if not did_overlap:
            not_overlapping_claims.add(claim.id)
        else:
            not_overlapping_claims.difference_update(overlapped)
            not_overlapping_claims.discard(claim.id)
    return overlap, not_overlapping_claims
