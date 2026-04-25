from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import Optional

DEFAULT_TZ = "UTC"

def utc_to_local(utc_dt: datetime, target_tz: str = DEFAULT_TZ) -> datetime:
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    try:
        tz = ZoneInfo(target_tz)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo(DEFAULT_TZ)
    return utc_dt.astimezone(tz)

def local_to_utc(local_dt: datetime, source_tz: str = DEFAULT_TZ) -> datetime:
    try:
        tz = ZoneInfo(source_tz)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo(DEFAULT_TZ)
    aware = local_dt.replace(tzinfo=tz)
    return aware.astimezone(timezone.utc)

def format_dt(dt: datetime, fmt: str = "%Y-%m-%d %H:%M", tz: str = DEFAULT_TZ) -> str:
    return utc_to_local(dt, tz).strftime(fmt)

def parse_utc(date_str: str, source_tz: str = DEFAULT_TZ) -> datetime:
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            return local_to_utc(dt, source_tz)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return datetime.now(timezone.utc)