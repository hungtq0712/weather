from __future__ import annotations

import argparse
import json
import sys

from app.clients.weather_api import OpenWeatherClient
from app.config import settings
from app.models import WeatherQuery
from app.services.city_service import CityService
from app.services.weather_service import WeatherService


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="app",
        description="City CRUD + Current Weather (OpenWeather).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # ---- city CRUD ----
    city = sub.add_parser("city", help="Quản lý danh sách thành phố")
    city_sub = city.add_subparsers(dest="city_cmd", required=True)

    add = city_sub.add_parser("add", help="Tạo thành phố")
    add.add_argument("--name", required=True, help='VD: "Hanoi"')
    add.add_argument("--country")
    add.add_argument("--state")
    add.add_argument("--lat", type=float)
    add.add_argument("--lon", type=float)

    city_sub.add_parser("list", help="List các thành phố")

    upd = city_sub.add_parser("update", help="Update thông tin thành phố")
    upd.add_argument("--id", type=int, required=True)
    upd.add_argument("--name")
    upd.add_argument("--country")
    upd.add_argument("--state")
    upd.add_argument("--lat", type=float)
    upd.add_argument("--lon", type=float)

    dele = city_sub.add_parser("delete", help="Xóa thành phố")
    dele.add_argument("--id", type=int, required=True)

    # ---- weather FR1 ----
    w = sub.add_parser("weather", help="Tra cứu thời tiết hiện tại (FR1)")
    w.add_argument("--city", help="Tên thành phố")
    w.add_argument("--id", type=int, help="Id thành phố đã lưu")
    w.add_argument("--lat", type=float, help="Vĩ độ")
    w.add_argument("--lon", type=float, help="Kinh độ")
    w.add_argument("--api-key", type=str, default=None, help="OpenWeather API key (ưu tiên hơn ENV)")
    w.add_argument("--units", type=str, default=None, help="metric | imperial | standard")
    w.add_argument("--lang", type=str, default=None, help="vi | en | ...")


    #---- hom khac ---
    w_sub = w.add_subparsers(dest="weather_cmd", required=True)
    y=w_sub.add_parser("yesterday", help="Tra cuu thoi tiet hom qua")
    y=w_sub.add_parser("tomorrow", help="Tra cuu thoi tiet ngay mai")

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    city_service = CityService()

    try:
        if args.cmd == "city":
            if args.city_cmd == "add":
                c = city_service.create_city(args.name, args.country, args.state, args.lat, args.lon)
                print(f"OK: created id={c.id} name={c.name}")
                return 0

            if args.city_cmd == "list":
                cities = city_service.list_cities()
                if not cities:
                    print("(empty)")
                    return 0
                for c in cities:
                    print(f"{c.id}: {c.name} | {c.state or ''} {c.country or ''} | lat={c.lat} lon={c.lon}")
                return 0

            if args.city_cmd == "update":
                c=city_service.update_city(
                    args.id,
                    name=args.name,
                    country=args.country,
                    state=args.state,
                    lat=args.lat,
                    lon=args.lon,
                )
                print(f"OK: updated id={c.id} name={c.name}")
                return 0

            if args.city_cmd == "delete":
                city_service.delete_city(args.id)
                print(f"OK: deleted id={args.id}")
                return 0

        if args.cmd == "weather":
            api_key = (args.api_key or settings.API_KEY).strip()
            if not api_key:
                print("ERROR: Thiếu API key. Hãy set OPENWEATHER_API_KEY hoặc truyền --api-key.", file=sys.stderr)
                return 1

            units = (args.units or settings.DEFAULT_UNITS).strip()
            lang = (args.lang or settings.DEFAULT_LANG).strip()

            client = OpenWeatherClient(settings.BASE_URL, api_key, settings.TIMEOUT_SECONDS)
            svc = WeatherService(client, city_service=city_service, units=units, lang=lang)

            q = WeatherQuery(id=args.id, city=args.city, lat=args.lat, lon=args.lon)

            # Nếu user chỉ muốn FR1 theo city string, dùng:
            # result = svc.get_current_by_city(args.city)
            result = svc.get_current_by_query(q)
            out_path = "weather_output.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(json.dumps(result, ensure_ascii=False, indent=2))


        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
