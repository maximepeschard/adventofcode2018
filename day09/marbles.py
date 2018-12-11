from typing import Tuple, Dict
import re


def parse_game_setup(description: str) -> Tuple[int, int]:
    """
    Parse a game setup (number of players and last marble value) from
    its description.
    """
    match = re.match(r"(?P<players>\d+)\D+(?P<last_marble>\d+).*", description)
    if not match:
        raise Exception("invalid game setup description")
    parsed = match.groupdict()
    return int(parsed["players"]), int(parsed["last_marble"])


class MarbleCircle:
    """Circular doubly linked representation of a game circle"""

    def __init__(
        self, value: int, prev: "MarbleCircle" = None, next: "MarbleCircle" = None
    ) -> None:
        self.value = value
        self.prev = prev if prev else self
        self.next = next if next else self

    def insertAfter(self, offset: int, value: int) -> "MarbleCircle":
        index, current = 0, self
        while index < offset:
            index += 1
            current = current.next
        new_node = MarbleCircle(value, current, current.next)
        current.next.prev = new_node
        current.next = new_node
        return new_node

    def removeBefore(self, offset: int) -> Tuple[int, "MarbleCircle"]:
        index, current = 0, self
        while index < offset:
            index += 1
            current = current.prev
        current.prev.next = current.next
        current.next.prev = current.prev
        return current.value, current.next

    def __str__(self) -> str:
        current, first = self, self
        str_circle = f"[*{self.value:02}]-->"
        while current.next != first:
            current = current.next
            str_circle += f"[{current.value:02}]-->"
        return str_circle


def highest_score(players: int, last_marble: int) -> int:
    """Compute the highest score of all players after the last marble is played"""
    scores: Dict[int, int] = {}
    circle = MarbleCircle(0)
    player = 0
    for marble in range(1, last_marble + 1):
        player = (player % players) + 1
        if marble % 23 == 0:
            removed, circle = circle.removeBefore(7)
            scores[player] = scores.get(player, 0) + marble + removed
        else:
            circle = circle.insertAfter(1, marble)
    return max(scores.values())
