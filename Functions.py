import os 
import json

file_path = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(file_path,"data cleaner/cache.json")

def load_json():
    with open(cache_path,'r') as file:
        data = file.read()
        data = json.loads(data)
    return dict(data)

def print_data(mipyme_name:str):
    #specific data from a mipyme
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
    #to get the mypime names
    json = load_json()
    keys = []
    for key in json.keys():
        keys.append(key)
    return keys

def data_to_list():
    #convert data to a list of dictionaries
    data = load_json()
    data_list = []
    for name,values in data.items():
        for key,value in values.items():
            if key == "products_info":
                for index in range(len(value["Products"])):
                    dicti = {
                        "mipyme_name":name,
                        "date":values["date"],
                        "time":values["time"],
                        "geolocation":values["geolocation"],
                        "township":values["township"],
                        "product":value["Products"][index],
                        "price":value["Prices"][index],
                        "units":value["Units"][index],
                        "exchange_rate":values["exchange_rate"]
                    }
                    data_list.append(dicti)
    return data_list

def print_data_list():
    #for visualize all data in data list
    for i in data_to_list():
        for key,value in i.items():
            print(key,": ",end="")
            print(value)

def filter_by(category, value):
    #to isolate data 
    #all data of a mipyme
    #all prices of a product
    data_list = data_to_list()
    filtred_list = []
    if category == "product":
        for key in data_list:
            if value.lower() in key["product"].lower():
                filtred_list.append(key["price"])
    elif category == "mipyme":
        for mipymes in data_list:
            if mipymes["mipyme_name"] == value:
                product = mipymes["product"]
                price = mipymes["price"]
                filtred_list.append((product,price))
    return filtred_list





