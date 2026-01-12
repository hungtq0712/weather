from __future__ import annotations

from typing import Any, Dict, Optional

from app.clients.base import BaseClient
from app.clients.errors import ApiResponseError


class OpenWeatherClient:
    """
    OpenWeather Current Weather (2.5):
      GET /data/2.5/weather?q=...&appid=...
      GET /data/2.5/weather?lat=...&lon=...&appid=...
    """

    def __init__(self, base_url: str, api_key: str, timeout: float) -> None:
        if not api_key:
            raise ValueError("Thiếu API key. Hãy set OPENWEATHER_API_KEY hoặc truyền --api-key.")
        self.api_key = api_key
        self._http = BaseClient(base_url, timeout)

    def current_by_city(self, city: str, units: str = "metric", lang: str = "vi") -> Dict[str, Any]:
        params = {"q": city, "appid": self.api_key, "units": units, "lang": lang}
        data = self._http.get_json("/data/2.5/weather", params=params)
        self._raise_if_openweather_error(data)
        return data

    def current_by_coords(self, lat: float, lon: float, units: str = "metric", lang: str = "vi") -> Dict[str, Any]:
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": units, "lang": lang}
        data = self._http.get_json("/data/2.5/weather", params=params)
        self._raise_if_openweather_error(data)
        return data

    @staticmethod
    def _raise_if_openweather_error(data: Dict[str, Any]) -> None:
        # OpenWeather dùng 'cod' để báo lỗi (có thể là int hoặc string)
        cod = data.get("cod")
        try:
            cod_int = int(cod)
        except Exception:
            cod_int = None

        if cod_int is not None and cod_int != 200:
            raise ApiResponseError(
                message=str(data.get("message") or "OpenWeather trả về lỗi."),
                status_code=cod_int,
                payload=data,
            )
