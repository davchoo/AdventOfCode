import re
from operator import itemgetter
import itertools
from more_itertools import first_true, zip_offset, flatten
import collections


def process_data(data: str):
    regex = re.compile(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)")
    all_events = list(map(lambda x: regex.match(x).groups(), data.splitlines()))
    all_events.sort(key=itemgetter(0, 1, 2, 3, 4))  # Sort chronologically by date and time

    # Groups by the same date, but adds the last hour of the previous day
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def grouping(event):
        year, month, day, hour, minute, text = event
        day = int(day)
        month = int(month)
        if hour == "23":
            day += 1
            if day > days_in_month[month]:
                day = 1
                month += 1
        return year, month, day

    events_by_date = itertools.groupby(all_events, key=grouping)
    guards = collections.defaultdict(lambda: collections.defaultdict(dict))

    for date, events in events_by_date:
        events = list(events)
        guard_shift_event = first_true(events, lambda x: "Guard" in x[5])[5]
        guard_id = int(re.findall(r"#(\d+)", guard_shift_event)[0])
        sleep_wake_events = sorted(filter(lambda x: x[3] == "00", events), key=itemgetter(4))

        for minute in range(60):
            guards[guard_id][date][minute] = False

        for start, end in zip_offset(sleep_wake_events, sleep_wake_events, offsets=[0, 1]):
            for minute in range(int(start[4]), int(end[4])):
                guards[guard_id][date][minute] = "asleep" in start[5]

    return guards


def find_frequent_sleep_minute(schedules):
    # The number of times the guard falls asleep on a given minute
    minute_asleep_pairs = flatten(map(lambda x: x.items(), schedules.values()))  # (minute, is asleep)
    minute_asleep = collections.Counter(filter(lambda x: x[1], minute_asleep_pairs))
    if len(minute_asleep) == 0:
        return -1, -1
    (minute, _), times_asleep = max(minute_asleep.items(), key=itemgetter(1))
    return minute, times_asleep


def solve_a(data):
    guards = process_data(data)
    total_minutes_asleep = {}
    for guard_id, schedules in guards.items():
        stats = collections.Counter(flatten(map(lambda x: x.values(), schedules.values())))
        total_minutes_asleep[guard_id] = stats[True]
    # Guard who slept the most
    guard_id, minutes_asleep = max(total_minutes_asleep.items(), key=itemgetter(1))
    minute, times_asleep = find_frequent_sleep_minute(guards[guard_id])
    return guard_id * minute


def solve_b(data):
    guards = process_data(data)
    frequent_sleep_minute = {}
    for guard_id, schedules in guards.items():
        minute, times_asleep = find_frequent_sleep_minute(guards[guard_id])
        frequent_sleep_minute[guard_id] = (minute, times_asleep)

    guard_id, (minute, times_asleep) = max(frequent_sleep_minute.items(), key=lambda x: x[1][1])
    return guard_id * minute
