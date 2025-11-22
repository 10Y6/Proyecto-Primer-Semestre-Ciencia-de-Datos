#get automatically date and time
import json
import datetime
import os

route_path = os.path.dirname(os.path.abspath(__file__))
route = os.path.join(route_path,"exchange_rate.json")

def date_time(date):
    #return the current date
    #for now ignore the time
    if isinstance(date,str):
        date = datetime.datetime.strptime(date,"%Y-%m-%d")
    date_time = date.strftime("%H:%M")
    date_date = date.strftime(r"%Y-%m-%d")
    with open(route,'r') as file:
        data = file.read()
        data = json.loads(data)
        data = data[f"{date_date}"]
    dict_ =  {
        "date":date_date,
        #"time":date_time,
        "exchange_rate":data
    }
    return dict_

#manualy get
#products, prices, unit

def get_product():
    products = []
    prices = []
    units = []
    while True:
        product = input("product: ")
        if product == "-1":break
        price = input("price: ")
        unit = input("unit: ")
        products.append(product)
        prices.append(price)
        units.append(unit)
    return {
        "products":products,
        "prices":prices,
        "units":units
    }