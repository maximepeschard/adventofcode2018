from typing import NamedTuple, Optional, Sequence, Tuple, Set
import re
import time


INITIAL_STATE_REGEX = re.compile(r"initial state:\s+(?P<init>[\.#]+)")
RULE_REGEX = re.compile(r"(?P<pattern>[\.#]{5})\s+=>\s+(?P<result>[\.#])")


class SpreadRule(NamedTuple):
    pattern: str
    produces: bool


def parse_initial_state(line: str) -> Optional[str]:
    """Parse a line describing the initial state of the plants"""
    match = INITIAL_STATE_REGEX.match(line)
    if not match:
        return None
    return match.groupdict()["init"]


def parse_rule(line: str) -> Optional[SpreadRule]:
    """Parse a line describing a spreading rule"""
    match = RULE_REGEX.match(line)
    if not match:
        return None
    parsed = match.groupdict()
    return SpreadRule(parsed["pattern"], parsed["result"] == "#")


def parse_notes(lines: Sequence[str]) -> Tuple[Set[SpreadRule], str]:
    """Parse notes and return a set of rules and an initial state"""
    init = ""
    rules = set()
    for line in lines:
        if not init:
            parsed_init = parse_initial_state(line)
            if parsed_init:
                init = parsed_init
                continue
        parsed_rule = parse_rule(line)
        if parsed_rule:
            rules.add(parsed_rule)
    return rules, init


def print_generation(pots: str, offset: int) -> None:
    """Pretty print a generation of pots, with plant zero in square brackets"""
    print(
        "\r"
        + "".join(
            [
                f"[{c}]" if i == offset else c
                for i, c in enumerate(pots)
                if i >= offset or c != "."
            ]
        ),
        end="",
        flush=True,
    )


def pad_pots(pots: str) -> Tuple[str, int]:
    """
    Add leading and trailing empty pots if needed, and return the number
    of empty pots prepended alongside the new pots.

    Example:
        >>> pad_pots("..#.#")
        (".....#.#.....", 3)
    """
    empty_left, empty_right, size = 0, 0, len(pots)
    index = 0
    while index < size and pots[index] == ".":
        empty_left += 1
        index += 1
    index = size - 1
    while index >= 0 and pots[index] == ".":
        empty_right += 1
        index -= 1
    offset_left, offset_right = max(0, 5 - empty_left), max(0, 5 - empty_right)
    return "".join(("." * offset_left, pots, "." * offset_right)), offset_left


def sum_planted_pots(
    rules: Set[SpreadRule], init: str, generations: int, display: bool = False
) -> int:
    """
    Compute the sum of the numbers of all pots which contain a plant after
    `generations` generations, given an initial state and a set of rules.

    For large `generations`, turning on display (`display=True`) shows that
    after a finite number of generations, the pots containing plants are just
    shifted to the right at each iteration. Once we detect this, we can break
    and compute the final sum.
    """
    producing_patterns = {
        f"(?={re.escape(rule.pattern)})" for rule in rules if rule.produces
    }
    producing_re = re.compile("|".join(producing_patterns))

    pots, offset = pad_pots(init)
    previous_producing: Set[int] = set()
    if display:
        print_generation(pots, offset)
        time.sleep(0.01)
    for generation in range(1, generations + 1):
        producing = {match.start() + 2 for match in producing_re.finditer(pots)}
        if producing == {i + 1 for i in previous_producing}:
            # now everything will just be shifted indefinitely
            return sum(i + generations - generation - offset for i in producing)
        previous_producing = producing
        new_pots = "".join("#" if i in producing else "." for i in range(len(pots)))
        pots, added = pad_pots(new_pots)
        offset += added
        if display:
            print_generation(pots, offset)
            time.sleep(0.01)

    return sum(index - offset for index in range(len(pots)) if pots[index] == "#")
