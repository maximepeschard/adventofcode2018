from common import Test, run_test_cases
from .fabric import Claim, parse_claim, overlapping


TEST_CLAIMS_DESCRIPTIONS = ["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]

TESTS = [
    Test(parse_claim, (TEST_CLAIMS_DESCRIPTIONS[0],), Claim(1, 1, 3, 4, 4)),
    Test(parse_claim, (TEST_CLAIMS_DESCRIPTIONS[1],), Claim(2, 3, 1, 4, 4)),
    Test(parse_claim, (TEST_CLAIMS_DESCRIPTIONS[2],), Claim(3, 5, 5, 2, 2)),
    Test(
        overlapping, ([parse_claim(c) for c in TEST_CLAIMS_DESCRIPTIONS], 2), (4, {3})
    ),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
