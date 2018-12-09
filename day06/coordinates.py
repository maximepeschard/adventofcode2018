from typing import NamedTuple, Sequence, Set, Dict, Tuple
import sys
import re
from functools import reduce


class Coordinate(NamedTuple):
    x: int
    y: int


class Boundaries(NamedTuple):
    top: int
    bottom: int
    left: int
    right: int


def parse_coordinate(description: str) -> Coordinate:
    """Parse a coordinate from its description"""
    parts = re.split(r"\s*,\s*", description)
    return Coordinate(int(parts[0]), int(parts[1]))


def manhattan_distance(p: Coordinate, q: Coordinate) -> int:
    """Compute the Manhattan distance between two coordinates"""
    return abs(p.x - q.x) + abs(p.y - q.y)


def find_boundaries(coordinates: Sequence[Coordinate]) -> Boundaries:
    """
    Compute the respective smallest and largest `x` and `y` values from
    a list of coordinates.
    """
    top, left = sys.maxsize, sys.maxsize
    bottom, right = 0, 0
    for c in coordinates:
        top = min(top, c.y)
        left = min(left, c.x)
        bottom = max(bottom, c.y)
        right = max(right, c.x)
    return Boundaries(top, bottom, left, right)


def compare(
    location: Coordinate, coordinates: Sequence[Coordinate]
) -> Tuple[Set[Coordinate], int]:
    """
    Compare a location to each coordinate of a list, computing :
    * the set of closest coordinates
    * the sum of the distances from the location to each coordinate
    """
    closest_coords: Set[Coordinate] = set()
    min_dist = sys.maxsize
    total_dists = 0
    for coord in coordinates:
        dist = manhattan_distance(coord, Coordinate(location.x, location.y))
        total_dists += dist
        if dist < min_dist:
            closest_coords = {coord}
            min_dist = dist
        elif dist == min_dist:
            closest_coords.add(coord)
    return (closest_coords if len(closest_coords) == 1 else set(), total_dists)


def sizes(coordinates: Sequence[Coordinate], region_threshold: int) -> Tuple[int, int]:
    """
    Compute the size of the largest finite area and the size of the region
    containing all locations with a sum of distances smaller than the given
    `region_threshold`.
    """
    boundaries = find_boundaries(coordinates)
    areas: Dict[Coordinate, int] = {}
    region_size = 0

    # We first determine coordinates with infinite areas : these are the
    # coordinates closest to the locations at the boundaries.
    closest_top = reduce(
        set.union,
        (
            compare(Coordinate(x, boundaries.top), coordinates)[0]
            for x in range(boundaries.left, boundaries.right + 1)
        ),
    )
    closest_bottom = reduce(
        set.union,
        (
            compare(Coordinate(x, boundaries.bottom), coordinates)[0]
            for x in range(boundaries.left, boundaries.right + 1)
        ),
    )
    closest_left = reduce(
        set.union,
        (
            compare(Coordinate(boundaries.left, y), coordinates)[0]
            for y in range(boundaries.top, boundaries.bottom + 1)
        ),
    )
    closest_right = reduce(
        set.union,
        (
            compare(Coordinate(boundaries.right, y), coordinates)[0]
            for y in range(boundaries.top, boundaries.bottom + 1)
        ),
    )
    infinite = closest_top | closest_bottom | closest_left | closest_right

    # Then we can compare each location inside the boundaries to the
    # coordinates and compute the sizes.
    for x in range(boundaries.left, boundaries.right + 1):
        for y in range(boundaries.top, boundaries.bottom + 1):
            closest_coordinates, total_dists = compare(Coordinate(x, y), coordinates)
            if total_dists < region_threshold:
                region_size += 1
            if len(closest_coordinates) != 1 or any(
                c in infinite for c in closest_coordinates
            ):
                continue
            for c in closest_coordinates:
                areas[c] = areas.get(c, 0) + 1

    return max(areas.values()), region_size
