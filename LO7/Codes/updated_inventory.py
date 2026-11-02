import json
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

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
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
    """Interface-style ABC — only shippable products implement this."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


# ======================
# PHYSICAL PRODUCT
# ======================
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weightkg):
        super().__init__(product_id, name, price, stock)
        self.__weightkg = weightkg

    def get_weight(self) -> float:
        return self.__weightkg

    # Override + reuse parent via super()
    def display_information(self):
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weightkg} kg")

    # Abstract method implementations
    def get_fulfillment_info(self) -> str:
        return f"Requires physical shipping ({self.__weightkg} kg)."

    def calculate_shipping_cost(self) -> float:
        # $5 base + $2 per kg
        return round(5.0 + 2.0 * self.__weightkg, 2)


# ======================
# DIGITAL PRODUCT
# ======================
class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, downloadable_size):
        super().__init__(product_id, name, price, stock)
        self.__downloadsize = downloadable_size

    def get_download_size(self) -> float:
        return self.__downloadsize

    def display_information(self):
        super().display_information()
        print(f"Type: Digital | Download Size: {self.__downloadsize} MB")

    def get_fulfillment_info(self) -> str:
        return f"Delivered electronically ({self.__downloadsize} MB download)."


# ======================
# INVENTORY
# ======================
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
            print(f"\nFulfillment: {p.get_fulfillment_info()}")

    def get_all_products(self):
        return list(self.__products)

    def total_shipping_cost(self) -> float:
        """Uses the interface — only shippable items contribute."""
        total = 0.0
        for p in self.__products:
            if isinstance(p, CanBeShipped):
                total += p.calculate_shipping_cost()
        return round(total, 2)


# ==============================
# FILE HANDLING (JSON)
# ==============================
def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("inventory.json not found — starting with an empty inventory.")
        return []
    except json.JSONDecodeError:
        print("inventory.json is corrupted — starting with an empty inventory.")
        return []

    products = []
    for row in data:
        try:
            ptype = row["type"]
            pid   = str(row["productid"]).strip()
            name  = str(row["name"]).strip()
            price = float(row["price"])
            stock = int(row["stock"])

            if ptype == "physical":
                products.append(
                    PhysicalProduct(pid, name, price, stock, float(row["weight"]))
                )
            elif ptype == "digital":
                products.append(
                    DigitalProduct(pid, name, price, stock, float(row["download_size"]))
                )
            else:
                print(f"Skipping unknown product type: {ptype}")
        except (KeyError, ValueError, TypeError) as e:
            print(f"Skipping bad record: {row} ({e})")
    return products


def save_inventory(inventory):
    data = []
    for p in inventory.get_all_products():
        base = {
            "productid": p.get_product_id(),
            "name":      p.get_name(),
            "price":     p.get_price(),
            "stock":     p.get_stock(),
        }
        if isinstance(p, PhysicalProduct):
            base["type"]   = "physical"
            base["weight"] = p.get_weight()
        elif isinstance(p, DigitalProduct):
            base["type"]          = "digital"
            base["download_size"] = p.get_download_size()
        data.append(base)

    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory successfully saved ({len(data)} products) to inventory.json.")


def handle_add_product(inventory):
    print("\n--- Add New Product ---")
    print("1. Physical Product")
    print("2. Digital Product")

    ptype = input("Choose type (1/2): ").strip()
    if ptype not in ("1", "2"):
        print("FAILED: Invalid product type.")
        return

    pid = input("Enter product ID: ").strip()
    if pid == "":
        print("FAILED: Product ID cannot be empty.")
        return

    name = input("Enter product name: ").strip()
    if name == "":
        print("FAILED: Product name cannot be empty.")
        return

    try:
        price = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))
    except ValueError:
        print("FAILED: Invalid number entered.")
        return

    if price < 0 or stock < 0:
        print("FAILED: Price and stock cannot be negative.")
        return

    try:
        if ptype == "1":
            weight = float(input("Enter weight (kg): "))
            if weight < 0:
                print("FAILED: Weight cannot be negative.")
                return
            product = PhysicalProduct(pid, name, price, stock, weight)
        else:
            size = float(input("Enter download size (MB): "))
            if size < 0:
                print("FAILED: Download size cannot be negative.")
                return
            product = DigitalProduct(pid, name, price, stock, size)
    except ValueError:
        print("FAILED: Invalid numeric input.")
        return

    if inventory.add_product(product):
        print(f"SUCCESS: Product '{name}' added to memory.")
        save_inventory(inventory)
    else:
        print(f"FAILED: Product ID '{pid}' already exists.")


def handle_update_stock(inventory):
    print("\n--- Update Stock ---")
    pid = input("Enter product ID: ").strip()
    product = inventory.search_product(pid)

    if product is None:
        print(f"Error: Product ID {pid} not found!")
        return

    try:
        new_stock = int(input("Enter new stock quantity: "))
    except ValueError:
        print("Invalid quantity. Please enter a whole number.")
        return

    if product.update_stock(new_stock):   # fixed typo: upate_stock -> update_stock
        print(f"Stock for {product.get_name()} updated to {new_stock} in memory.")
        save_inventory(inventory)


def handle_search(inventory):
    print("\n--- Search Product ---")
    pid = input("Enter product ID: ").strip()
    product = inventory.search_product(pid)

    if product is None:
        print(f"Error: Product ID {pid} not found!")
        return

    print("Product Found:")
    product.display_information()
    print(f"Fulfillment: {product.get_fulfillment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")


def handle_shipping_total(inventory):
    print(f"\nTotal shipping cost of inventory: ${inventory.total_shipping_cost():.2f}")


def main():
    inventory = Inventory()

    for product in load_inventory():
        inventory.add_product(product)

    while True:
        print("\n===========================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("===========================")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Total Shipping Cost")
        print("0. Exit")
        print("----------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Current Inventory ---")
            inventory.display_all()
        elif choice == "2":
            handle_add_product(inventory)
        elif choice == "3":
            handle_update_stock(inventory)
        elif choice == "4":
            handle_search(inventory)
        elif choice == "5":
            handle_shipping_total(inventory)
        elif choice == "0":
            print("Goodbye!")
            print(f"Total Records in JSON: {len(inventory.get_all_products())}")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 5.")


if __name__ == "__main__":
    main()