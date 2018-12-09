from typing import NamedTuple, Optional, Sequence, List, Dict
from enum import Enum
from dataclasses import dataclass
import re
from datetime import datetime


class Action(Enum):
    BEGIN_SHIFT = "begins shift"
    FALL_ASLEEP = "falls asleep"
    WAKE_UP = "wakes up"


class Record(NamedTuple):
    date: datetime
    guard: Optional[int]
    action: Action


def parse_record(record: str) -> Record:
    """Parse a guard observation record"""
    match = re.match(
        r"^\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hour>\d{2}):(?P<minute>\d{2})\]\s+([a-zA-Z]+\s+#(?P<guard>\d+)\s+)?(?P<action>.+)$",
        record,
    )
    if not match:
        raise Exception("invalid record")
    parsed = match.groupdict()
    date = datetime(
        int(parsed["year"]),
        int(parsed["month"]),
        int(parsed["day"]),
        int(parsed["hour"]),
        int(parsed["minute"]),
    )
    guard = parsed.get("guard")
    if guard:
        return Record(date, int(guard), Action(parsed["action"]))
    else:
        return Record(date, None, Action(parsed["action"]))


@dataclass
class GuardStat:
    total: int
    minutes: List[int]


def guard_stats(records: Sequence[Record]) -> Dict[int, GuardStat]:
    guard: int
    date_asleep: datetime
    stats: Dict[int, GuardStat] = {}
    for record in sorted(records, key=lambda r: r.date):
        if record.action == Action.BEGIN_SHIFT:
            if not record.guard:
                raise Exception("invalid begin shift")
            else:
                guard = record.guard
            if guard not in stats:
                stats[guard] = GuardStat(0, [0] * 60)
        elif record.action == Action.FALL_ASLEEP:
            date_asleep = record.date
        elif record.action == Action.WAKE_UP:
            stats[guard].total += record.date.minute - date_asleep.minute
            stats[guard].minutes[date_asleep.minute] += 1
            stats[guard].minutes[record.date.minute] -= 1
    return stats


def strategy_1(stats: Dict[int, GuardStat]) -> int:
    guard, _ = sorted(stats.items(), key=lambda kv: kv[1].total, reverse=True)[0]
    minutes = stats[guard].minutes
    current, most_aslept_minute, most_aslept_minute_value = 0, 0, 0
    for minute, value in enumerate(minutes):
        current += value
        if current > most_aslept_minute_value:
            most_aslept_minute = minute
            most_aslept_minute_value = current
    return most_aslept_minute * guard


def strategy_2(stats: Dict[int, GuardStat]) -> int:
    nb_asleep_max = 0
    guard_asleep_max = 0
    minute_asleep_max = 0
    for guard, guard_stat in stats.items():
        minutes = stats[guard].minutes
        current, most_aslept_minute, most_aslept_minute_value = 0, 0, 0
        for minute, value in enumerate(minutes):
            current += value
            if current > most_aslept_minute_value:
                most_aslept_minute = minute
                most_aslept_minute_value = current
        if most_aslept_minute_value > nb_asleep_max:
            nb_asleep_max = most_aslept_minute_value
            guard_asleep_max = guard
            minute_asleep_max = most_aslept_minute
    return minute_asleep_max * guard_asleep_max
