"""
from itertools import product
from typing import Union
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

products = [
    Product(id=1, name="Phone", description="A budget smartphone", price=149.99, quantity=60),
    Product(id=2, name="Laptop", description="A lightweight student laptop", price=599.00, quantity=25),
    Product(id=3, name="Headphones", description="Wireless over-ear headphones", price=79.90, quantity=120),
    Product(id=4, name="Smartwatch", description="Fitness tracking smartwatch", price=129.50, quantity=45),
    Product(id=5, name="Tablet", description="10-inch Android tablet", price=199.99, quantity=35),
    Product(id=6, name="Router", description="Dual-band Wi-Fi router", price=54.99, quantity=80),
    Product(id=7, name="Keyboard", description="Mechanical keyboard (blue switch)", price=45.00, quantity=70),
    Product(id=8, name="Mouse", description="Wireless ergonomic mouse", price=19.99, quantity=150),
    Product(id=9, name="Powerbank", description="20000mAh fast-charging power bank", price=34.50, quantity=90),
    Product(id=10, name="Speaker", description="Portable Bluetooth speaker", price=49.00, quantity=55),
]


@app.get("/products")
def get_products():
    return products
@app.get("/product/{id}")
def get_product(id: int):
    return products[id-1]


@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product/{id}")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if(products[i].id == id):
            products[i]= product
"""

from itertools import product
from typing import Union
from pydantic import BaseModel

import argparse
import json
import sys

from app.clients.weather_api import OpenWeatherClient
from app.config import settings
from app.models import WeatherQuery
from app.services.city_service import CityService
from app.services.weather_service import WeatherService
from app.models import City

from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def read_root():
    return {"Current weather"}



@app.get("/cities")
def get_cities():
    city_service = CityService()
    return city_service.list_cities()
@app.get("/city/{id}")
def get_city(id: int):
    city_service = CityService()
    return city_service.find_by_id(id)
@app.get("/weather/{name}")
def get_weather(name: str):
    api_key =  settings.API_KEY.strip()
    city_service = CityService()
    units = settings.DEFAULT_UNITS.strip()
    lang =  settings.DEFAULT_LANG.strip()

    client = OpenWeatherClient(settings.BASE_URL, api_key, settings.TIMEOUT_SECONDS)
    svc = WeatherService(client, city_service=city_service, units=units, lang=lang)
    result = svc.get_current_by_city(name)
    return result

@app.post("/city")
def add_city(city: City):
    city_service = CityService()
    return city_service.create_city(city.name, city.country, city.state, city.lat, city.lon)

@app.put("/city/{id}")
def update_city(id: int, city: City):
    city_service = CityService()
    city_service.update_city(id,city.name, city.country, city.state, city.lat, city.lon)
@app.delete("/city/{id}")
def delete_city(id: int):
    city_service = CityService()
    city_service.delete_city(id)
