from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List


# -------- Persist model (CRUD) --------
@dataclass(frozen=True)
class City:
    id: int
    name: str
    country: Optional[str] = None
    state: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


# -------- Query model (rule) --------
@dataclass(frozen=True)
class WeatherQuery:
    """
    Rule: hoặc city hoặc (lat & lon).
    id: tham chiếu thành phố đã lưu (nếu user chọn từ list).
    """
    id: Optional[int] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    days: Optional[int] = None
    def __post_init__(self) -> None:
        has_city = bool(self.city and self.city.strip())
        has_latlon = (self.lat is not None) and (self.lon is not None)

        if has_city and has_latlon:
            raise ValueError("WeatherQuery invalid: chỉ được chọn city hoặc (lat & lon), không được cả hai.")
        if (not has_city) and (not has_latlon) and (self.id is None):
            raise ValueError("WeatherQuery invalid: cần id hoặc city hoặc cả lat & lon.")


# -------- FR1 Output models --------
@dataclass(frozen=True)
class LocationOut:
    name: str
    country: Optional[str] = None


@dataclass(frozen=True)
class CurrentOut:
    temperature: Optional[float] = None
    feels_like: Optional[float] = None
    humidity: Optional[int] = None
    wind: Optional[float] = None
    description: Optional[str] = None
    observed_at: Optional[str] = None  # ISO string


@dataclass(frozen=True)
class WeatherCurrentResponse:
    location: LocationOut
    current: CurrentOut
    source: str
