import datetime
import zoneinfo
import os
import sys

class TimezoneManager:
    def __init__(self):
        self.system_tz = self._detect_system_tz()
        self.user_tz = self.system_tz

    def _detect_system_tz(self):
        if sys.platform == "win32":
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation")
                tz_name = winreg.QueryValueEx(key, "TimeZoneKeyName")[0]
                return tz_name if tz_name else "UTC"
            except Exception:
                return "UTC"
        else:
            tz_env = os.environ.get("TZ")
            if tz_env:
                return tz_env
            try:
                return str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)
            except Exception:
                return "UTC"

    def set_user_tz(self, tz_name: str):
        try:
            zoneinfo.ZoneInfo(tz_name)
            self.user_tz = tz_name
        except zoneinfo.ZoneInfoNotFoundError:
            pass

    def get_user_tz(self) -> str:
        return self.user_tz

    def utc_to_user(self, dt: datetime.datetime) -> datetime.datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        try:
            return dt.astimezone(zoneinfo.ZoneInfo(self.user_tz))
        except zoneinfo.ZoneInfoNotFoundError:
            return dt.astimezone(datetime.timezone.utc)

    def user_to_utc(self, dt: datetime.datetime) -> datetime.datetime:
        try:
            tz = zoneinfo.ZoneInfo(self.user_tz)
        except zoneinfo.ZoneInfoNotFoundError:
            tz = datetime.timezone.utc
        aware = dt.replace(tzinfo=tz) if dt.tzinfo is None else dt.astimezone(tz)
        return aware.astimezone(datetime.timezone.utc)

    def format_datetime(self, dt: datetime.datetime, fmt: str = "%Y-%m-%d %H:%M", use_local: bool = True) -> str:
        target = self.utc_to_user(dt) if use_local else dt
        return target.strftime(fmt)

    def parse_iso_to_utc(self, iso_str: str) -> datetime.datetime:
        try:
            dt = datetime.datetime.fromisoformat(iso_str)
            if dt.tzinfo is None:
                return self.user_to_utc(dt)
            return dt.astimezone(datetime.timezone.utc)
        except ValueError:
            return datetime.datetime.now(datetime.timezone.utc)