from .product import Product, CanBeShipped

# ======================
# PHYSICAL PRODUCT
# ======================
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weightkg):
        super().__init__(product_id, name, price, stock)
        self.__weightkg = weightkg

    def get_weight(self) -> float:
        return self.__weightkg

    def display_information(self):
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weightkg} kg")

    def get_fulfillment_info(self) -> str:
        return f"Requires physical shipping ({self.__weightkg} kg)."

    def calculate_shipping_cost(self) -> float:
        return round(5.0 + 2.0 * self.__weightkg, 2)