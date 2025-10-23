from models import Mipyme
import json
import os.path as path
import os

to_do_route =  os.path.dirname(os.path.abspath(__file__))
cache_route = os.path.join(to_do_route,"cache.json")

mipyme = Mipyme()

while True:
    mipyme.name = input("name")
    if mipyme.name == "-1":break
    mipyme.date = input("date")
    mipyme.time = input("time")
    mipyme.geoloc = input("geoloc")
    mipyme.township = input("township")
    mipyme.products_prices = input("products_prices")
    mipyme.exchange_rate = input("exchange_rate")  
    mipyme.add_mipyme()
