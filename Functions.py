import os 
import json

#group and normalize datas

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
                if 'pelly' in data['product'] and cath=='carnicos':continue
                if 'refresco' in data['product'] and cath == 'carnicos':continue
                if 'alubias' in data['product'] and cath == 'carnicos':continue
                if 'ron' in data['product'] and cath == 'carnicos':continue
                if 'cerveza' in data['product'] and cath == 'carnicos':continue
                if 'salchi' in data['product'] and cath == 'viveres':continue
                if 'salmon' in data['product'] and cath == 'viveres':continue
                
                
                grouped.append(data)
    return grouped
   
def group_and_norm(data,cath):
    own_data = group_products(cath,data)
    own_data = [{'date':x['date'],
                          'product':x['product'],
                          'price':round(x['price']/x['unit'][0],2),
                          'unit':(1,x['unit'][1])} 
                            for x in own_data]
    return own_data
            
    
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
        "pescado":'pescado',
        'huevos':'huevos',
        'huevo':'huevos',
        'aceite':'aceite'
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
        
    units = ['lata','paquete','huevos','huevo','tubo','pqt','caja',
             'cajita','cabeza','unidad','unidades','bolsa','pote',
             'pomo','botella','barra']
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
            number = round(float(text) * 0.453,2)
        except:
            number = 0.453
    elif 'g' in text and not 'kg' in text:
        unit = "kg"
        text = text.strip()
        text = text.strip('g')
        number = round(float(text) * 0.001,2)
    elif 'ml' in text:
        unit = "L"
        text = text.strip()
        text = text.strip('ml')
        try:
            number = round(float(text) * 0.001,2)
        except:
            number = 1
    elif 'kg' in text:
        unit = "kg"
        text = text.strip()
        text = text.strip('kg')
        try:
            number = round(float(text),2)
        except:
            number = 1
    elif 'l' in text or 'L' in text:
        unit = "L"
        text = text.strip()
        text = text.strip('l')
        text = text.strip('L')
        try:
            number = round(float(text),2)
        except:
            number = 1
    
    return (number,unit)

def normalize_numbers(texto):
    return round(float(texto),2)

#utilities functions

def merge_data(data_1,data_2):
    data = data_1.copy()
    data.extend(data_2)
    return data

def CS(value_list):
    #calculate statitics 
    len_list = len(value_list)
    if len_list == 0:return -1
    value_list = sorted(value_list)
    mean = sum(value_list)/len_list
    median = sum(value_list[len_list//2-1:len_list//2])/2 if len_list % 2 == 0 else value_list[len_list//2]
    range_ = abs(min(value_list)-max(value_list))
    variance = sum([(x-mean)**2 for x in value_list])/(len_list)
    standard_deviation = variance**(1/2)
    return {
        "mean":round(mean,2),
        "median":round(median,2),
        "range":round(range_,2),
        "variance":round(variance,2),
        "standard_deviation":round(standard_deviation,2),
    }

#data_in_situ functions
def load_json():
    file_path = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(file_path,"data_in_situ/db_in_situ.json")
    
    with open(cache_path,'r') as file:
        data = file.read()
        data = json.loads(data)
    return dict(data)

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
                        "date":myp_info["date"],
                        "product":normalize_text(value["Products"][index]),
                        "price":normalize_numbers((value["Prices"][index])),
                        "unit":normalize_units(value["Units"][index]),
                    }
                    data_list.append(dicti)
    return data_list

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
    return data
