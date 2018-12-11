from typing import NamedTuple, Sequence, Dict, Set, List
import re


class Velocity(NamedTuple):
    x: int
    y: int


class Point(NamedTuple):
    x: int
    y: int
    v: Velocity


def parse_point(description: str) -> Point:
    """Parse a point location and velocity from its description"""
    match = re.match(
        r"\D+<\s*(?P<x>-?\d+),\s*(?P<y>-?\d+)>\D+<\s*(?P<vx>-?\d+),\s*(?P<vy>-?\d+)>",
        description,
    )
    if not match:
        raise Exception("invalid point")
    parsed = match.groupdict()
    return Point(
        int(parsed["x"]),
        int(parsed["y"]),
        Velocity(int(parsed["vx"]), int(parsed["vy"])),
    )


def move(point: Point, second: int) -> Point:
    """Get a point properties after `second` seconds"""
    return Point(point.x + second * point.v.x, point.y + second * point.v.y, point.v)


def display(points: Sequence[Point]) -> None:
    """Print a representation of a sequence of points"""
    xs = [point.x for point in points]
    ys = [point.y for point in points]
    for y in range(min(ys), max(ys) + 1):
        line: List[str] = []
        for x in range(min(xs), max(xs) + 1):
            if any(p.x == x and p.y == y for p in points):
                line += "#"
            else:
                line += "."
        print("".join(line))


def message(points: Sequence[Point]) -> int:
    """
    Move points until a message appear and return the time it took.

    We consider a message has appeared when we find a "column" with at
    least 8 consecutive points.
    """
    second = 0
    message_appeared = None

    while not message_appeared:
        cols: Dict[int, Set[int]] = {}
        moved_points = [move(point, second) for point in points]
        for point in moved_points:
            if point.x in cols:
                cols[point.x].add(point.y)
            else:
                cols[point.x] = {point.y}
        for col, ys in cols.items():
            previous_y = -1
            aligned = 0
            max_aligned = 0
            for y in sorted(ys):
                if y == previous_y + 1:
                    aligned += 1
                else:
                    max_aligned = max(max_aligned, aligned)
                    aligned = 0
                previous_y = y
            if aligned > 0:
                max_aligned = max(max_aligned, aligned)
            if max_aligned >= 8:
                message_appeared = True
                display(moved_points)
                break
        if not message_appeared:
            second += 1

    return second
