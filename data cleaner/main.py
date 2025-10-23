from models import Mipyme

mipyme = Mipyme()

while True:
    mipyme.name = input("name: ")
    if mipyme.name == "-1":break
    mipyme.date = input("date: ")
    mipyme.time = input("time: ")
    mipyme.geoloc = input("geoloc: ")
    mipyme.township = input("township: ")
    for i in range(10):
        #nombre
        #magnitud/unidad *recordar estandarizar*
        #precio
        #marca si la tiene
        mipyme.products_info.append(input("products_info: "))
    mipyme.exchange_rate = input("exchange_rate")  
    mipyme.add_mipyme()
