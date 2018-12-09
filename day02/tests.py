from common import Test, run_test_cases
from .inventory import classify_candidate, checksum, common_letters_prototype


TESTS = [
    Test(classify_candidate, ("abcdef",), (0, 0)),
    Test(classify_candidate, ("bababc",), (1, 1)),
    Test(classify_candidate, ("abbcde",), (1, 0)),
    Test(classify_candidate, ("abcccd",), (0, 1)),
    Test(classify_candidate, ("aabcdd",), (1, 0)),
    Test(classify_candidate, ("abcdee",), (1, 0)),
    Test(classify_candidate, ("ababab",), (0, 1)),
    Test(
        checksum,
        (["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"],),
        12,
    ),
    Test(
        common_letters_prototype,
        (["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"],),
        "fgij",
    ),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
