import os
from pathlib import Path
from typing import NamedTuple, Callable, Any, Sequence


root = Path(os.path.dirname(os.path.realpath(__file__)))


class Test(NamedTuple):
    function: Callable
    input: tuple
    expected: Any


def run_test_cases(cases: Sequence[Test], verbose: bool = False) -> None:
    for case in cases:
        try:
            output = case.function(*case.input)
            assert output == case.expected
        except AssertionError:
            print(
                f"[X] {case.function.__name__}: expected {case.expected} for input {case.input}, found {output}"
            )
        else:
            if verbose:
                print(f"[√] {case.function.__name__}{case.input} == {case.expected}")
