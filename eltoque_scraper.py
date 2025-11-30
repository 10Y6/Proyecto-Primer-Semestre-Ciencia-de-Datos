import json
import requests
import os

file_route = os.path.dirname(os.path.abspath(__file__))
db_exch_route = os.path.join(file_route,'db_exch_rate.json')
raw_route = os.path.join(file_route,'api_raw.json')

base_url = 'https://api.cambiocuba.money/api/v1/x-rates-by-date-range-history?trmi=true&cur=USD&token=aCY78gC3kWRv1pR7VfgSlg&period=730D'

response = requests.get(base_url)
response = response.json()

with open(raw_route,'w') as file:
    file.write(json.dumps(response,indent=4))

with open(db_exch_route,'w') as file:
    dict_ = {}
    for i in response:
        dict_[f"{i['_id']}"] = i['median']
    
    aux = []
    for i in dict_.items():
        aux.append(i)
    aux.sort()
    dict_ = {}
    for i in aux:
        dict_[i[0]] = i[1]
    
    file.write(json.dumps(dict_,indent=4))
        

