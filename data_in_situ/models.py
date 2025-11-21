import os.path as path
import os
import json

#json route
to_do_route =  os.path.dirname(os.path.abspath(__file__))
cache_route = os.path.join(to_do_route,"cache_real.json")




class Mipyme():
    def __init__(self,name=None,date=None,time=None,geoloc=None,
                 township=None,products_info=[],exchange_rate=" "):
        self.name = name 
        self.date = date
        self.time = time
        self.geoloc = geoloc
        self.township = township
        self.products_info = products_info
        
        exchange_rate_route = os.path.dirname(os.path.abspath(__file__))
        exchange_rate_route = os.path.join(exchange_rate_route,"../")
        exchange_rate_route_abs = os.path.join(exchange_rate_route,"exchange_rate.json")
        
        with open(exchange_rate_route_abs,'r') as file: 
            aux = json.loads(file.read())
            self.exchange_rate = aux[f"{self.date}"]
        
    
    def create_mipyme(self):
        mipyme = {
            self.name : {
                'date':self.date,
                'time':self.time,
                'geolocation':self.geoloc,
                'township':self.township,
                'products_info':self.products_info,
                'exchange_rate':self.exchange_rate
            }
        }
        return mipyme
    
    def add_mipyme(self):
        dictio = {}
        with open(cache_route,'r') as file:
                dictio = file.read()
                dictio = json.loads(dictio)
        
        with open(cache_route,'w') as file:
            dicti = self.create_mipyme()
            dictio.update(dicti)
            file.write(json.dumps(dictio,indent=4))