import json
from data_fill import date_time as dt
from data_fill import get_product as gp
import datetime
import os

route_path = os.path.dirname(os.path.abspath(__file__))
route = os.path.join(route_path,"cache_facebook.json")

def create_data(date):
    data = dt(date)
    ans = {}
    product_info = gp()
    ans[data["date"]] = {
        "time": data["time"],
        "exchange_rate": data["exchange_rate"],
        "products":product_info["products"],
        "prices":product_info["prices"],
        "units":product_info["units"]
    }
    return ans
    
def add_data(new_data):
    with open(route,"r") as file:
        file = file.read()
        data = json.loads(file)
    
    new_data_key = next(iter(new_data.keys()))
    if new_data_key in data.keys():
        data[new_data_key]["products"].extend(new_data[new_data_key]["products"])
        data[new_data_key]["prices"].extend(new_data[new_data_key]["prices"])
        data[new_data_key]["units"].extend(new_data[new_data_key]["units"])
    else:
        data.update(new_data)

    with open(route,"w") as file:
        file.write(json.dumps(data,indent=4))

add_data(create_data("2025-10-25"))
