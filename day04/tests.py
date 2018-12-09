from common import Test, run_test_cases
from datetime import datetime
from .guards import Action, Record, parse_record, guard_stats, strategy_1


TEST_RECORDS = [
    "[1518-11-01 00:00] Guard #10 begins shift",
    "[1518-11-01 00:05] falls asleep",
    "[1518-11-01 00:25] wakes up",
    "[1518-11-01 00:30] falls asleep",
    "[1518-11-01 00:55] wakes up",
    "[1518-11-01 23:58] Guard #99 begins shift",
    "[1518-11-02 00:40] falls asleep",
    "[1518-11-02 00:50] wakes up",
    "[1518-11-03 00:05] Guard #10 begins shift",
    "[1518-11-03 00:24] falls asleep",
    "[1518-11-03 00:29] wakes up",
    "[1518-11-04 00:02] Guard #99 begins shift",
    "[1518-11-04 00:36] falls asleep",
    "[1518-11-04 00:46] wakes up",
    "[1518-11-05 00:03] Guard #99 begins shift",
    "[1518-11-05 00:45] falls asleep",
    "[1518-11-05 00:55] wakes up",
]

TESTS = [
    Test(
        parse_record,
        (TEST_RECORDS[0],),
        Record(datetime(1518, 11, 1, 0, 0), 10, Action.BEGIN_SHIFT),
    ),
    Test(
        parse_record,
        (TEST_RECORDS[1],),
        Record(datetime(1518, 11, 1, 0, 5), None, Action.FALL_ASLEEP),
    ),
    Test(
        parse_record,
        (TEST_RECORDS[2],),
        Record(datetime(1518, 11, 1, 0, 25), None, Action.WAKE_UP),
    ),
    Test(strategy_1, (guard_stats([parse_record(r) for r in TEST_RECORDS]),), 240),
]


def run(verbose: bool = False) -> None:
    run_test_cases(TESTS, verbose)
