#get automatically date and time
import json
import datetime
import os

exch_rate = os.path.dirname(os.path.abspath(__file__))
exch_rate = os.path.join(exch_rate,"../")
exch_rate_route = os.path.join(exch_rate,"db_exch_rate.json")

def date_time(date):
    if isinstance(date,str):
        date = datetime.datetime.strptime(date,"%Y-%m-%d")
    date_date = date.strftime(r"%Y-%m-%d")
    with open(exch_rate_route,'r') as file:
        data = file.read()
        data = json.loads(data)
        data = data[f"{date_date}"]
    dict_ =  {
        "date":date_date,
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
        "unit":units
    }