import os 
import json

file_path = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(file_path,"data cleaner/cache.json")

aux1 = "date time geolocation township products_info exchange_rate"
aux2 = "Products Prices Units"
global_keys = aux1.split(sep=" ")

"""
products_info
    Products
    Prices
    Units
"""
def load_json():
    with open(cache_path,'r') as file:
        data = file.read()
        data = json.loads(data)
    return dict(data)

def print_data(mipyme_name:str):
    data = load_json()[mipyme_name]
    for key, value in data.items():
        if key == "products_info":
            print("Products_info")
            products = value["Products"]
            prices = value["Prices"]
            units = value["Units"]
            spc_sep = max(len(x) for x in products)
            spc_sep2 = max(len(x) for x in prices)
            for index in range(len(value["Products"])):
                print(products[index]," "*(spc_sep-len(products[index])),end="")
                print(prices[index]," "*(spc_sep2-len(prices[index])),end="")
                print(units[index])
        else:
            print(key,": ",sep="",end="")
            print(value)

def get_keys():
    json = load_json()
    keys = []
    for key in json.keys():
        keys.append(key)
    return keys
        
print_data("Bodega El Mambi")



