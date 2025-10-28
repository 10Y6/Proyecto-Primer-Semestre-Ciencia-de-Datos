
class Manager():
    def __init__(self,product_name=None,product_price=None,
                 product_unit=None,product_quant=None):
        self.product_name = product_name
        self.product_price = product_price
        self.produce_unit = product_unit
        self.product_quant = product_quant
        
    def product_board(self):
        self.product_quant = int(input("product_quant: "))
        aux_name = []
        aux_price = []
        aux_unit = []
        for _ in range(self.product_quant):
            self.product_name = input("product_name: ")
            self.product_price = input("product_price: ")
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
        