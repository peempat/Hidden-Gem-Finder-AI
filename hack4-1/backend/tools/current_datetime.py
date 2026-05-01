"""
current_datetime.py
Provides the current date and time for travel planning.
"""

from datetime import datetime, timedelta, timezone as fixed_timezone
from zoneinfo import ZoneInfo


def _get_timezone(timezone_name: str):
    if not timezone_name:
        timezone_name = "Asia/Bangkok"

    try:
        return timezone_name, ZoneInfo(timezone_name)
    except Exception:
        if timezone_name in {"Asia/Bangkok", "Bangkok", "Thailand"}:
            return "Asia/Bangkok", fixed_timezone(timedelta(hours=7), name="Asia/Bangkok")

        local_tz = datetime.now().astimezone().tzinfo
        return "local system timezone", local_tz


def current_datetime(timezone: str = "Asia/Bangkok") -> dict:
    """
    Return the current date and time for the requested timezone.

    Args:
        timezone: IANA timezone name. Defaults to Asia/Bangkok.

    Returns:
        dict: Current date/time fields and helpful relative-date references.
    """
    timezone, tz = _get_timezone(timezone)

    now = datetime.now(tz)
    tomorrow = now + timedelta(days=1)
    next_week = now + timedelta(days=7)

    return {
        "timezone": timezone,
        "iso_datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
        "month": now.month,
        "month_name": now.strftime("%B"),
        "year": now.year,
        "day": now.day,
        "human_readable": now.strftime("%A, %B %d, %Y at %H:%M:%S"),
        "relative_dates": {
            "today": now.strftime("%Y-%m-%d"),
            "tomorrow": tomorrow.strftime("%Y-%m-%d"),
            "next_week": next_week.strftime("%Y-%m-%d"),
            "current_month": now.strftime("%B"),
            "current_year": now.year,
        },
    }
