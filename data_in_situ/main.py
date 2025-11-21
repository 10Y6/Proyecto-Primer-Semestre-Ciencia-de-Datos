from models import Mipyme
from product_manager import Manager

manager = Manager()

while True:
    #inputs
    name = input("name: ")
    if name == "-1":break
    date = input("date: ")
    time = input("time: ")
    geoloc = input("geoloc: ")
    township = input("township: ")
    products_info = manager.product_board()
    #
    mipyme = Mipyme(name,date,time,geoloc,township,products_info=products_info)
    print(mipyme.exchange_rate)
    mipyme.add_mipyme()