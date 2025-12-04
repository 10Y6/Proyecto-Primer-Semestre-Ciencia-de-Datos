import json
import os
import datetime

from data_fill import date_time as dt
from data_fill import get_product as gp

route_path = os.path.dirname(os.path.abspath(__file__))
route = os.path.join(route_path,"db_online.json")

def create_data(date):
    if not date:date = datetime.datetime.now()
    #return -1 to break the cicle if the user need it
    if date == "-1":return -1
    data = dt(date)
    ans = {}
    product_info = gp()
    ans[data["date"]] = {
        #"time": data["time"],
        #"exchange_rate": data["exchange_rate"],
        "products":product_info["products"],
        "prices":product_info["prices"],
        "unit":product_info["unit"]
    }
    return ans
    
def add_data(new_data):
    #return -1 if the user need break the cicle
    if new_data == -1:return -1
    with open(route,"r") as file:
        file = file.read()
        data = json.loads(file)
    
    new_data_key = next(iter(new_data.keys()))
    if new_data_key in data.keys():
        data[new_data_key]["products"].extend(new_data[new_data_key]["products"])
        data[new_data_key]["prices"].extend(new_data[new_data_key]["prices"])
        data[new_data_key]["unit"].extend(new_data[new_data_key]["unit"])
    else:
        data.update(new_data)

    with open(route,"w") as file:
        file.write(json.dumps(data,indent=4))