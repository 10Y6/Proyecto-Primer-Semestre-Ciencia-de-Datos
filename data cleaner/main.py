from models import Mipyme
from product_manager import Manager

mipyme = Mipyme()
manager = Manager()

while True:
    mipyme.name = input("name: ")
    if mipyme.name == "-1":break
    mipyme.date = input("date: ")
    mipyme.time = input("time: ")
    mipyme.geoloc = input("geoloc: ")
    mipyme.township = input("township: ")
    mipyme.products_info = manager.product_board()
    mipyme.exchange_rate = input("exchange_rate: ")  
    mipyme.add_mipyme()
