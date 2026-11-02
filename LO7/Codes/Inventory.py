from Models.product import CanBeShipped


class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for p in self.__products:
            if p.get_product_id() == product_id:
                return p
        return None

    def display_all(self):
        if not self.__products:
            print("Inventory Empty")
            return
        for p in self.__products:
            p.display_information()
            print(f"Fulfillment: {p.get_fulfillment_info()}\n")

    def get_all_products(self):
        return list(self.__products)

    def total_shipping_cost(self) -> float:
        total = 0.0
        for p in self.__products:
            if isinstance(p, CanBeShipped):
                total += p.calculate_shipping_cost()
        return round(total, 2)