from __future__ import annotations

from typing import Any, Dict, Mapping, Optional
import requests

from app.clients.errors import ApiResponseError


class BaseClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get_json(self, path: str, params: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        url = self._url(path)
        try:
            resp = self._session.get(url, params=params, timeout=self.timeout)
        except requests.RequestException as e:
            raise ApiResponseError(f"Lỗi mạng/timeout: {e}") from e

        if resp.status_code >= 400:
            raise ApiResponseError(
                message="API trả về lỗi HTTP",
                status_code=resp.status_code,
                payload=(resp.text[:2000] if resp.text else None),
            )

        try:
            data = resp.json()
        except ValueError as e:
            raise ApiResponseError("API trả về không phải JSON hợp lệ", status_code=resp.status_code) from e

        if not isinstance(data, dict):
            raise ApiResponseError("JSON sai định dạng (cần object/dict).", payload=data)
        return data
