from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.config import settings
from app.models import City
from app.utils.storage import *
from app.utils.validate import validate_city


class CityService:
    def __init__(self, file_path: str = settings.CITIES_FILE,file_path_data = settings.DATA_BASE) -> None:
        self._file = file_path
        self._file_data_base = settings.DATA_BASE

    def list_cities(self) -> List[City]:
        return [self._dict_to_city(x) for x in load_json_list(self._file)]

    def create_city(
        self,
        name: str,
        country: Optional[str] = None,
        state: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> City:
        name_norm = validate_city(name)
        items = load_json_list(self._file)
        next_id = max([int(it.get("id", 0)) for it in items], default=0) + 1

        city = City(id=next_id, name=name_norm, country=country, state=state, lat=lat, lon=lon)
        items.append(self._city_to_dict(city))
        save_json_list(self._file, items)
        return city

    def update_city(self, city_id: int, **patch: Any) -> City:
        items = load_json_list(self._file)
        for i, it in enumerate(items):
            if int(it.get("id")) == int(city_id):
                if "name" in patch and patch["name"] is not None:
                    patch["name"] = validate_city(str(patch["name"]))
                it.update({k: v for k, v in patch.items() if v is not None})
                items[i] = it
                save_json_list(self._file, items)
                return self._dict_to_city(it)
        raise ValueError(f"Không tìm thấy thành phố id={city_id}")

    def delete_city(self, city_id: int) -> None:
        items = load_json_list(self._file)
        new_items = [it for it in items if int(it.get("id")) != int(city_id)]
        if len(new_items) == len(items):
            raise ValueError(f"Không tìm thấy thành phố id={city_id}")
        save_json_list(self._file, new_items)

    def get_by_id(self, city_id: int) -> City:
        items = load_json_list(self._file)
        for it in items:
            if int(it.get("id")) == int(city_id):
                return self._dict_to_city(it)
        raise ValueError(f"Không tìm thấy thành phố id={city_id}")

    @staticmethod
    def _city_to_dict(c: City) -> Dict[str, Any]:
        return {
            "id": c.id,
            "name": c.name,
            "country": c.country,
            "state": c.state,
            "lat": c.lat,
            "lon": c.lon,
        }

    @staticmethod
    def _dict_to_city(d: Dict[str, Any]) -> City:
        return City(
            id=int(d["id"]),
            name=str(d["name"]),
            country=d.get("country"),
            state=d.get("state"),
            lat=d.get("lat"),
            lon=d.get("lon"),
        )
    #-----DATA BASE-----#
    def create_city(
        self,
        name: str,
        country: Optional[str] = None,
        state: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> City:
        name_norm = validate_city(name)
        id= self.next_id()
        city = City(id=id, name=name_norm, country=country, state=state, lat=lat, lon=lon)
        add_database(self._file_data_base, self._city_to_dict(city))
        return city

    def update_city(self, id: int,
        name: str,
        country: Optional[str] = None,
        state: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,) -> City:
        name_norm = validate_city(name)
        city = City(id=id, name=name_norm, country=country, state=state, lat=lat, lon=lon)
        update_database(self._file_data_base, self._city_to_dict(city),id)
        return city
    def delete_city(self, city_id: int) -> None:
        delete_database(self._file_data_base, city_id)
    def list_cities(self) -> List[City]:

        return [self._dict_to_city(x) for x in load_database(self._file_data_base)]

    def find_by_id(self,id: int) -> Dict[str, Any]:

        conn = create_connection()

        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM {TABLE} WHERE id={id}")
        rows = cur.fetchall()

        data = [dict(r) for r in rows]

        conn.close()
        return data[0]

    def next_id(self) -> int:
        conn = create_connection()
        # conn = sqlite3.connect(path)
        try:
            cur = conn.cursor()

            # 1) Ưu tiên lấy AUTO_INCREMENT (nếu có)
            cur.execute(
                """
                SELECT AUTO_INCREMENT
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = %s
                """,
                (TABLE,),
            )
            row = cur.fetchone()
            if row and row[0] is not None:
                return int(row[0])

            # 2) Fallback: MAX(id) + 1
            cur.execute(f"SELECT COALESCE(MAX(`id`), 0) + 1 FROM `{TABLE}`")
            (nid,) = cur.fetchone()
            return int(nid)

        finally:
            conn.close()