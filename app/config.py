from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class settings:
    """
    Cấu hình chung:
    - api_key: lấy từ ENV OPENWEATHER_API_KEY (khuyến nghị), hoặc truyền qua CLI --api-key
    - base_url: OpenWeather API base
    - timeout: thời gian chờ HTTP
    - units: metric/imperial/standard
    - lang: ngôn ngữ mô tả thời tiết (vi/en/...)
    """
    CITIES_FILE: str = "cities.json"
    DATA_BASE: str = "cities.db"
    BASE_URL: str = "https://api.openweathermap.org"
    TIMEOUT_SECONDS: float = 10.0

    # mặc định dùng metric (Celsius)
    DEFAULT_UNITS: str = "metric"
    DEFAULT_LANG: str = "vi"

    # Lấy API key từ biến môi trường
    API_KEY = "30d4741c779ba94c470ca1f63045390a"
