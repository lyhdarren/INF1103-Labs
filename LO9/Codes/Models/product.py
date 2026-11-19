from abc import ABC, abstractmethod
from Models.supplier import Supplier


# ======================
# PRODUCT (ABSTRACT)
# ======================
class Product(ABC):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ):
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        try:
            stock = int(stock)
        except (TypeError, ValueError):
            raise ValueError("Stock quantity must be a whole number.")
        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock

        # Store the Supplier object (association)
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, new_quantity: int) -> bool:
        try:
            new_quantity = int(new_quantity)
        except (TypeError, ValueError):
            raise ValueError("Stock quantity must be a whole number.")
        if new_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__stock = new_quantity
        return True

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

        print("\n--- Supplier Information ---")
        self.__supplier.display_information()

    @abstractmethod
    def get_fulfillment_info(self) -> str:
        pass


# ======================
# CAN BE SHIPPED (INTERFACE)
# ======================
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass