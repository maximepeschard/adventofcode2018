from typing import Dict, Tuple, Set, Sequence, List
from enum import Enum
from dataclasses import dataclass


class Track(Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    INTERSECTION = "+"
    CURVE_1 = "/"
    CURVE_2 = "\\"


class Turn(Enum):
    LEFT = -90
    STRAIGHT = 0
    RIGHT = 90


UP_ANGLE, RIGHT_ANGLE, DOWN_ANGLE, LEFT_ANGLE = 0, 90, 180, 270
DIRECTION_MAPPINGS = (
    ("^", UP_ANGLE),
    (">", RIGHT_ANGLE),
    ("v", DOWN_ANGLE),
    ("<", LEFT_ANGLE),
)


class Direction(Enum):
    UP = UP_ANGLE
    RIGHT = RIGHT_ANGLE
    DOWN = DOWN_ANGLE
    LEFT = LEFT_ANGLE

    @classmethod
    def from_char(cls, char: str) -> "Direction":
        for c, v in DIRECTION_MAPPINGS:
            if c == char:
                return Direction(v)
        raise Exception("invalid direction character")

    def apply_turn(self, turn: Turn) -> "Direction":
        return Direction((self.value + turn.value) % 360)

    def __str__(self) -> str:
        for c, v in DIRECTION_MAPPINGS:
            if self.value == v:
                return c
        raise Exception("unmapped direction")


Tracks = Dict[Tuple[int, int], Track]


def next_turn(turn: Turn) -> Turn:
    """Find the turn type a cart will have to make after the passed turn type"""
    turns = list(Turn)
    return turns[(turns.index(turn) + 1) % len(turns)]


@dataclass
class Cart:
    x: int
    y: int
    direction: Direction
    turn: Turn = Turn.LEFT

    def _ahead(self) -> Tuple[int, int]:
        if self.direction is Direction.UP:
            return self.x, self.y - 1
        elif self.direction is Direction.DOWN:
            return self.x, self.y + 1
        elif self.direction is Direction.LEFT:
            return self.x - 1, self.y
        else:
            return self.x + 1, self.y

    def move(self, tracks: Tracks) -> Tuple[int, int]:
        """Update location and direction given tracks, and return the new location"""
        ahead_x, ahead_y = self._ahead()
        ahead = tracks.get((ahead_x, ahead_y))
        if (
            ahead is Track.CURVE_1
            and self.direction in (Direction.RIGHT, Direction.LEFT)
            or ahead is Track.CURVE_2
            and self.direction in (Direction.UP, Direction.DOWN)
        ):
            self.direction = self.direction.apply_turn(Turn.LEFT)
        elif (
            ahead is Track.CURVE_1
            and self.direction in (Direction.UP, Direction.DOWN)
            or ahead is Track.CURVE_2
            and self.direction in (Direction.LEFT, Direction.RIGHT)
        ):
            self.direction = self.direction.apply_turn(Turn.RIGHT)
        elif ahead is Track.INTERSECTION:
            self.direction = self.direction.apply_turn(self.turn)
            self.turn = next_turn(self.turn)
        self.x = ahead_x
        self.y = ahead_y

        return ahead_x, ahead_y


def parse_map(map_lines: Sequence[str]) -> Tuple[Tracks, List[Cart]]:
    """Parse lines describing a map into tracks and carts objects"""
    tracks, carts = {}, []
    track_chars = {t.value for t in list(Track)}
    direction_chars = {str(d) for d in list(Direction)}

    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char in track_chars:
                tracks[x, y] = Track(char)
            elif char in direction_chars:
                carts.append(Cart(x, y, Direction.from_char(char)))
                if char in (str(Direction.UP), str(Direction.DOWN)):
                    tracks[x, y] = Track.VERTICAL
                else:
                    tracks[x, y] = Track.HORIZONTAL

    return tracks, carts


def display_map(tracks: Tracks, carts: List[Cart]) -> None:
    """Print a map representation with tracks and carts"""
    max_x, max_y = 0, 0
    for x, y in tracks.keys():
        max_x, max_y = max(x, max_x), max(y, max_y)

    grid = []
    for y in range(max_y + 1):
        line = [
            tracks[x, y].value if (x, y) in tracks else " " for x in range(max_x + 1)
        ]
        grid.append(line)

    seen: Set[Tuple[int, int]] = set()
    for cart in carts:
        if (cart.x, cart.y) in seen:
            grid[cart.y][cart.x] = "X"
        else:
            seen.add((cart.x, cart.y))
            grid[cart.y][cart.x] = str(cart.direction)

    grid_lines = ["".join(line) for line in grid]
    print("\n".join(grid_lines) + "\n")


def first_crash_location(
    tracks: Tracks, carts: List[Cart], display: bool = False
) -> Tuple[int, int]:
    """Compute the location of the first crash"""
    if display:
        display_map(tracks, carts)

    collision_location = None
    locations = {(c.x, c.y) for c in carts}
    while not collision_location:
        for cart in sorted(carts, key=lambda c: (c.y, c.x)):
            locations.discard((cart.x, cart.y))
            new_location = cart.move(tracks)
            if new_location in locations:
                collision_location = new_location
                break
            else:
                locations.add(new_location)
        if display:
            display_map(tracks, carts)

    return collision_location


def last_cart_location(
    tracks: Tracks, carts: List[Cart], display: bool = False
) -> Tuple[int, int]:
    """
    Compute the location of the last cart at the end of the first tick where
    it is the only cart left.
    """
    if display:
        display_map(tracks, carts)

    # `remaining_carts` contains the indexes of the remaining carts
    remaining_carts = set(range(len(carts)))
    # `locations` contains sets of cart indexes by location
    locations: Dict[Tuple[int, int], Set[int]] = {}
    for number, cart in enumerate(carts):
        locations[cart.x, cart.y] = locations.get((cart.x, cart.y), set()) | {number}

    while len(remaining_carts) > 1:
        numbered_carts = ((i, carts[i]) for i in remaining_carts)
        for number, cart in sorted(numbered_carts, key=lambda c: (c[1].y, c[1].x)):
            if number not in remaining_carts:
                # the cart was remaining at the beginning of the tick but another
                # one collided with it since then, and both were removed from
                # `remaining_carts` : we can skip
                continue
            locations[cart.x, cart.y].discard(number)
            new_location = cart.move(tracks)
            if locations.get(new_location, set()):
                remaining_carts -= locations[new_location] | {number}
                locations[new_location].clear()
            else:
                locations[new_location] = locations.get(new_location, set()) | {number}
        if display:
            display_map(tracks, [carts[i] for i in remaining_carts])

    last = carts[remaining_carts.pop()]
    return last.x, last.y
