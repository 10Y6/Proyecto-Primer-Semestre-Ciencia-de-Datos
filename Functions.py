import os 
import json

def load_json():
    file_path = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(file_path,"data cleaner/cache.json")
    
    with open(cache_path,'r') as file:
        data = file.read()
        data = json.loads(data)
    return dict(data)

def print_data(mipyme_name):
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
    #all products in a township
    data_list = data_to_list()
    filtred_list = []
    if category == "product":
        for key in data_list:
            if value.lower() in key["product"].lower():
                dicti = {
                    "price":key["price"],
                    "exchange_rate":key["exchange_rate"],
                    "township":key["township"],
                }
                filtred_list.append(dicti)
        return filtred_list
    elif category == "mipyme":
        for mipymes in data_list:
            if mipymes["mipyme_name"] == value:
                product = mipymes["product"]
                price = mipymes["price"]
                filtred_list.append((product,int(price)))
        return filtred_list
    elif category == "township":
        for key in data_list:
            if value.lower() == key["township"].lower():
                dicti = {
                    "product":key["product"],
                    "price":key["price"],
                    "exchange_rate":key["exchange_rate"],
                    "mipyme_name":key["mipyme_name"]
                }
                filtred_list.append(dicti)
        return filtred_list
                

def calculate_statistics(value_list):
    #calculate statitics 
    len_list = len(value_list)
    value_list = sorted(value_list)
    mean = sum(value_list)/len_list
    median = sum(value_list[len_list//2-1:len_list//2])/2 if len_list % 2 == 0 else value_list[len_list//2]
    range_ = abs(min(value_list)-max(value_list))
    variance = sum([(x-mean)**2 for x in value_list])/(len_list-1)
    standard_deviation = variance**(1/2)
    #mode for fix, improve in a future
    mode = [value_list.count(x) for x in value_list]
    #mode
    return {
        "mean":round(mean,2),
        "median":round(median,2),
        "range":round(range_,2),
        "mode":mode,
        "variance":round(variance,2),
        "standard_deviation":round(standard_deviation,2),
    }

def organize_by(category):
    #organize data by a categroy
    if category ==  "township":
        pass
    elif category == "product":
        pass
    elif category == "mipyme":
        pass
    
def product_vs_exchange(product_list,exchange_list):
    pass



