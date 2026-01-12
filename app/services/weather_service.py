from __future__ import annotations

from typing import Any, Dict, Optional

from app.clients.weather_api import OpenWeatherClient
from app.config import settings
from app.models import WeatherCurrentResponse, LocationOut, CurrentOut, WeatherQuery
from app.services.city_service import CityService
from app.utils.time import to_iso_observed_at
from app.utils.validate import validate_city


class WeatherService:
    SOURCE_NAME = "OpenWeatherMap"

    def __init__(
        self,
        client: OpenWeatherClient,
        city_service: Optional[CityService] = None,
        units: str = settings.DEFAULT_UNITS,
        lang: str = settings.DEFAULT_LANG,
    ) -> None:
        self._client = client
        self._city_service = city_service or CityService()
        self._units = units
        self._lang = lang


    # FR1 — Tra cứu thời tiết hiện tại theo thành phố
    def get_current_by_city(self, city: str) -> Dict[str, Any]:
        city_norm = validate_city(city)
        raw = self._client.current_by_city(city_norm, units=self._units, lang=self._lang)
        return self._map_fr1(raw)

    # Mở rộng theo WeatherQuery (id/city/latlon)
    def get_current_by_query(self, query: WeatherQuery) -> Dict[str, Any]:
        if query.id is not None:
            c = self._city_service.get_by_id(query.id)
            if c.lat is not None and c.lon is not None:
                raw = self._client.current_by_coords(c.lat, c.lon, units=self._units, lang=self._lang)
                return self._map_fr1(raw)
            # fallback: dùng name
            raw = self._client.current_by_city(c.name, units=self._units, lang=self._lang)
            return self._map_fr1(raw)

        if query.city is not None:
            return self.get_current_by_city(query.city)

        # lat/lon
        assert query.lat is not None and query.lon is not None
        raw = self._client.current_by_coords(query.lat, query.lon, units=self._units, lang=self._lang)
        return self._map_fr1(raw)

    def _map_fr1(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        # location
        name = str(raw.get("name") or "")
        sys_block = raw.get("sys") or {}
        country = sys_block.get("country")

        # current weather
        main = raw.get("main") or {}
        wind = raw.get("wind") or {}
        weather_list = raw.get("weather") or []

        description = None
        if isinstance(weather_list, list) and weather_list:
            w0 = weather_list[0] or {}
            # OpenWeather thường có description (tôn trọng lang param)
            description = w0.get("description") or w0.get("main")

        observed_at = to_iso_observed_at(raw.get("dt"), raw.get("timezone"))

        out = WeatherCurrentResponse(
            location=LocationOut(name=name, country=country),
            current=CurrentOut(
                temperature=main.get("temp"),
                feels_like=main.get("feels_like"),
                humidity=main.get("humidity"),
                wind=wind.get("speed"),
                description=description,
                observed_at=observed_at,
            ),
            source=self.SOURCE_NAME,
        )

        # JSON output đúng FR1
        return {
            "location": {
                "name": out.location.name,
                "country": out.location.country,
            },
            "weather": {
                "current": {
                    "temperature": out.current.temperature,
                    "feels_like": out.current.feels_like,
                    "humidity": out.current.humidity,
                    "wind": out.current.wind,
                    "description": out.current.description,
                    "observed_at": out.current.observed_at,
                }
            },
            "source": out.source,
        }
