import os 
import json

#data_in_situ functions
def load_json():
    file_path = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(file_path,"data_in_situ/db_in_situ.json")
    
    with open(cache_path,'r') as file:
        data = file.read()
        data = json.loads(data)
    return dict(data)

def normalize_text(text):
    text = text.lower().strip()
    types = {
        "pasta dental":"pasta dental",
        "perrito":"salchicha",
        'perritos':'salchicha',
        "perro":"salchicha",
        'perros':'salchicha',
        'perritos':'salchicha',
        "salchicha":"salchicha",
        "spaguettis":"spaguettis",
        'papel higienico':'papel higienico',
        'macarrones':'macarron',
        'macarron':'macarron',
        'codito':'macarron',
        'coditos':'macarron',
        'detergente':'detergente',
        "pescado":'pescado'
    }
    trans = str.maketrans('áéíóú','aeiou')
    text = text.translate(trans)
    for error,right in types.items(): 
        if error in text:
            text = right
            break   
    return text

def normalize_units(text):
    #lb to kg
    #g to kg
    #ml to L
    #unidades to u
    number = 0
    unit = ""
    #excepciones para unidades
    #lata,tubo,paquete,pqt
    units = ['lata','paquete','huevos','huevo','tubo','pqt'
             ,'unidad','unidades','bolsa','pote','pomo','botella']
    for exceptions in units:
        if exceptions in text:
            unit = "u"
            text = text.strip()
            text = text.strip('lata')
            text = text.strip('paquete')
            text = text.strip('tubo')
            text = text.strip('unidades')
            text = text.strip('unidad')
            
            try:
                number = float(text)
            except:
                number = 1
            return (number,unit)
        elif 'carton' in text:
            return (30,'u')
        
    #casos 
    if 'lb' in text or 'lbs' in text:
        unit = "kg"
        text = text.strip()
        text = text.strip('lbs')
        text = text.strip('lb')
        try:
            number = float(text) * 0.453
        except:
            number = 0.453
    elif 'g' in text and not 'kg' in text:
        unit = "kg"
        text = text.strip()
        text = text.strip('g')
        number = float(text) * 0.001
    elif 'ml' in text:
        unit = "L"
        text = text.strip()
        text = text.strip('ml')
        try:
            number = float(text) * 0.001
        except:
            number = 1
    elif 'kg' in text:
        unit = "kg"
        text = text.strip()
        text = text.strip('kg')
        try:
            number = float(text)
        except:
            number = 1
    elif 'l' in text or 'L' in text:
        unit = "L"
        text = text.strip()
        text = text.strip('l')
        text = text.strip('L')
        try:
            number = float(text)
        except:
            number = 1
    
    return (number,unit)

def normalize_numbers(texto):
    return round(float(texto),2)

def merge_online_situ(data_online,data_in_situ):
    data = data_in_situ.copy()
    data.extend(data_online)
    return data

def data_in_situ():
    #convert data to a list of dictionaries
    data = load_json()
    data_list = []
    for name,myp_info in data.items():
        for key,value in myp_info.items():
            if key == "products_info":
                for index in range(len(value["Products"])):
                    lat,lon = myp_info["geolocation"].split(',')
                    dicti = {
                        #"mipyme_name":normalize_text(name),
                        "date":myp_info["date"],
                        #"time":myp_info["time"],
                        #'lat':float(lat.strip()),
                        #'lon':float(lon.strip()),
                        #"township":normalize_text(myp_info["township"]),
                        "product":normalize_text(value["Products"][index]),
                        "price":normalize_numbers((value["Prices"][index])),
                        "unit":normalize_units(value["Units"][index]),
                        #"exchange_rate":normalize_numbers(myp_info["exchange_rate"])
                    }
                    data_list.append(dicti)
    return data_list

def group_products(cath,datas):
    #group all producst by category
    all_data = datas
    carnicos = [
        'pollo','cerdo','res','picadillo','salchicha',
        'perrito','jamon', 'lomo','chorizo','hamburguesa', 
        'pescado','atun','sierra','bonito','salmon', 
        'mortadella','bistec','higado','molleja','albondiga', 
        'croqueta','fiambre','span','masa','carne','salchichon'
    ]
    alcohol = ['cerveza','vino','ron','vodka','whisky','shaka']
    higiene = ['detergente','papel','toallitas humedas',
               'jabon','champu','desodorante',
               ]
    viveres = ['arroz','azucar','aceite','miel','harina','frijol',
               'chicharo','alubia','judia','mayonesa','mostaza',
               'pasta','ketchup','macarron','cafe','leche','pan',
               'fideo','vinagre','sal','pure']
    bebidas = ['malta','refresco','jugo','pepsi','cola']
    types = {
        'carnicos':carnicos,
        'alcohol':alcohol,
        'higiene':higiene,
        'bebidas':bebidas,
        'viveres':viveres
    }
    grouped = []
    for data in all_data:
        for target in types[cath]:
            if target in data['product']:
                grouped.append(data)
    return grouped
   

def filter_by(category, value):
    #to isolate data 
    #all data of a mipyme
    #all prices of a product
    #all products in a township
    data_list = data_in_situ()
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
    elif category == "mipyme":
        for mipymes in data_list:
            if mipymes["mipyme_name"] == value:
                product = mipymes["product"]
                price = mipymes["price"]
                filtred_list.append((product,float(price)))
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
    if len_list == 0:return -1
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
#

#onei functions

def load_json_onei(cath):
    file_route = os.path.dirname(os.path.abspath(__file__))
    min_max_route = os.path.join(file_route,'data_onei/min_max_prices.json')
    salary_route = os.path.join(file_route,'data_onei/salary_median.json')
    with open(salary_route,'r') as file:
       salary = file.read()
       salary = json.loads(salary)
    
    with open(min_max_route,'r') as file:
        min_max = file.read()
        min_max = json.loads(min_max)
    
    if cath =='min_max':return min_max
    return salary

def data_onei():
    #data from de onei to a standard list
    data = load_json_onei('min_max')
    list_ = []
    
    for date,products in data.items():
        dict_ = {}
        for product,info in products.items():
            if not info['min'] or not info['max']:continue
            dict_ = {
                'date':date,
                'product':normalize_text(product),
                'price':(info['min'] + info['max'])/2,
                'unit':normalize_units(info['unit'])
            }
            if 'aceite' in dict_['product']:
                dict_['unit'] = (dict_['unit'][0],'L')
            list_.append(dict_)
    
    return list_

#online functions

def load_online():
    file_route = os.path.dirname(os.path.abspath(__file__))
    online_route = os.path.join(file_route,'data_online/db_online.json')
    
    with open(online_route,'r') as file:
        data = file.read()
        data = json.loads(data)
    return data

def data_online():
    data = load_online()
    list_ = []
    for date,info in data.items():
        dict_ = {}
        for index in range(len(info['unit'])):
            dict_ = {
                'date':date,
                'product':normalize_text(info['products'][index]),
                'price':normalize_numbers(info['prices'][index]),
                'unit':normalize_units(info['unit'][index])
            }
            list_.append(dict_)
    return list_

def load_exch_rate():
    file_route = os.path.dirname(os.path.abspath(__file__))
    exch_route = os.path.join(file_route,'db_exch_rate.json')
    with open(exch_route,'r') as file:
        data = file.read()
        data = json.loads(data)
    list_ = []
    for i,j in data.items():
        list_.append({'date':i,'rate':j})
    return list_

#

#
#debug functions
#

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

def print_data_list():
    #for visualize all data in data list
    for i in data_in_situ():
        for key,value in i.items():
            print(key,": ",end="")
            print(value)