from abc import ABC, abstractmethod

# ======================
# PRODUCT (ABSTRACT)
# ======================
class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity):
        if quantity < 0:
            print(f"Error: Cannot set stock below 0 (requested: {quantity})")
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} "
              f"| Price: ${self.__price:.2f} | Stock: {self.__stock}")

    @abstractmethod
    def get_fulfillment_info(self) -> str:
        pass


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

