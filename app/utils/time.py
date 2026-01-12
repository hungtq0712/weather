from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Optional


def to_iso_observed_at(dt_utc: object, tz_offset_seconds: object) -> Optional[str]:
    """
    OpenWeather:
      - dt: unix UTC
      - timezone: offset seconds from UTC
    Ta trả về ISO-8601 local time.
    """
    try:
        dt_int = int(dt_utc)
        offset = int(tz_offset_seconds) if tz_offset_seconds is not None else 0
        tz = timezone(timedelta(seconds=offset))
        return datetime.fromtimestamp(dt_int, tz=tz).isoformat()
    except Exception:
        return None
