from common import Test, run_test_cases
from .steps import Requirement, parse_requirement, complete


TEST_INSTRUCTIONS = [
    "Step C must be finished before step A can begin.",
    "Step C must be finished before step F can begin.",
    "Step A must be finished before step B can begin.",
    "Step A must be finished before step D can begin.",
    "Step B must be finished before step E can begin.",
    "Step D must be finished before step E can begin.",
    "Step F must be finished before step E can begin.",
]

TESTS = [
    Test(parse_requirement, (TEST_INSTRUCTIONS[0],), Requirement("C", "A")),
    Test(
        complete,
        ([parse_requirement(r) for r in TEST_INSTRUCTIONS], 2, 0),
        ("CABFDE", 15),
    ),
    Test(
        complete,
        ([parse_requirement(r) for r in TEST_INSTRUCTIONS], 1, 0),
        ("CABDFE", 21),
    ),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
