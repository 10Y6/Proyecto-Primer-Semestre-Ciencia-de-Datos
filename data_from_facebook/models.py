import json
from data_fill import current_date_time as cdt
from data_fill import get_product as gp
import datetime
import os

route_path = os.path.dirname(os.path.abspath(__file__))
route = os.path.join(route_path,"cache_facebook.json")

def create_data(date):
   data = cdt(date)
   ans = {data : gp()}
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
    print(data)
    with open(route,"w") as file:
        file.write(json.dumps(data,indent=4))
