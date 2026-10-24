import json


# ======================
# PRODUCT CLASS
# ======================

class Product:
    """Responsibility: represent and manage a single product."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---- getters ----
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # ---- state management (encapsulation) ----
    def update_stock(self, quantity):
        """Apply a DELTA to stock. Product decides what is valid."""
        if self.__stock + quantity < 0:
            print(f"Error: Cannot reduce stock below 0 "
                  f"(current: {self.__stock}, requested: {quantity})")
            return
        self.__stock += quantity
        print(f"Stock updated. New stock for {self.__name}: {self.__stock}")

    def set_stock(self, quantity):
        """Set stock to an ABSOLUTE value. Product decides what is valid."""
        if quantity < 0:
            print(f"Error: Stock cannot be negative (requested: {quantity})")
            return
        self.__stock = quantity
        print(f"Stock updated. New stock for {self.__name}: {self.__stock}")

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )


# ======================
# INVENTORY CLASS
# ======================

class Inventory:
    """Responsibility: manage a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            print(f"Error: Product ID {product.get_product_id()} already exists!")
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for x in self.__products:
            if x.get_product_id() == product_id:
                return x
        return None

    def display_all(self):
        if not self.__products:
            print("Inventory Empty")
            return
        for x in self.__products:
            x.display_information()

    def get_all_products(self):
        return list(self.__products)

    def is_empty(self):
        return len(self.__products) == 0


# ==============================
# MAIN
# ==============================

def main():
    return


if __name__ == "__main__":
    main()