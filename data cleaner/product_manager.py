
class Manager():
    def __init__(self,product_name=None,product_price=None,
                 product_unit=None,product_quant=None):
        self.product_name = product_name
        self.product_price = product_price
        self.produce_unit = product_unit
        
    def product_board(self):
        aux_name = []
        aux_price = []
        aux_unit = []
        while True:
            self.product_name = input("product_name: ")
            if self.product_name == "-1":break
            
            self.product_price = str(round(eval(input("product_price: ")),2))
            self.product_unit = input("product_unit: ")
            aux_name.append(self.product_name)
            aux_price.append(self.product_price)
            aux_unit.append(self.product_unit)
        aux_dict = {
            "Products: ": aux_name,
            "Prices: " : aux_price,
            "Units: " : aux_unit
        }
        return aux_dict
        