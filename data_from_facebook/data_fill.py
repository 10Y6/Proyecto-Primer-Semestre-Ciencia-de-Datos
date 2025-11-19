#get automatically date and time

def current_date_time(date):
    #return the current date
    #for now ignore the time
    date_time = date.strftime("%H:%M")
    date_date = date.strftime(r"%Y:%m:%d")
    dict_ =  {
        "date":date_date,
        "time":date_time
    }
    return date_date

#manualy get
#products, prices, unit

def get_product():
    products = []
    prices = []
    units = []
    while True:
        product = input("product: ")
        if product == "-1":break
        price = input("price: ")
        unit = input("unit: ")
        products.append(product)
        prices.append(price)
        units.append(unit)
    return {
        "products":products,
        "prices":prices,
        "units":units
    }