from datetime import datetime, timedelta
from dateutil.rrule import rrulestr, rruleset
from typing import List

def expand_recurring(start_time: datetime, rule_str: str, window_start: datetime, window_end: datetime) -> List[datetime]:
    rs = rruleset()
    try:
        rule = rrulestr(rule_str, dtstart=start_time, ignoretz=True)
        rs.rrule(rule)
    except ValueError:
        return []
    return rs.between(window_start, window_end, inc=True)

def get_next_occurrences(start_time: datetime, rule_str: str, count: int = 10) -> List[datetime]:
    try:
        rule = rrulestr(rule_str, dtstart=start_time, ignoretz=True)
        return list(rule[:count])
    except ValueError:
        return []