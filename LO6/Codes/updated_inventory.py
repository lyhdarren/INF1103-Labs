import json

# ======================
# PRODUCT CLASS
# ======================
class Product:
    
    def __init__(self, product_id, name, price, stock):
        
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        
        return self.__product_id

    def get_name(self):
        
        return self.__name

    def get_price(self):
        
        return self.__price

    def get_stock(self):
        
        return self.__stock

    def update_stock(self, quantity):
        
        if (quantity < 0):
            
            print(f"Error: Cannot reduce stock below 0 requested: {quantity})")
            return False
        
        else:
            
            self.__stock = quantity
            return True

    def display_information(self):
        
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

# ======================
# INVENTORY CLASS
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
        
        for x in self.__products:
            
            if x.get_product_id() == product_id:
                
                return x
            
        return None

    def display_all(self):
        
        if self.__products == "":
            
            print("Inventory Empty")
            return
        
        for x in self.__products:
            x.display_information()

    def get_all_products(self):
        
        return list(self.__products)

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
            products.append(
                Product(
                    str(row["productid"]).strip(),
                    str(row["name"]).strip(),
                    float(row["price"]),
                    int(row["stock"]),
                )
            )
        except (KeyError, ValueError, TypeError) as e:
            print(f"Skipping bad record: {row} ({e})")
    return products


def save_inventory(inventory):

    data = [
        {
            "productid": p.get_product_id(),
            "name": p.get_name(),
            "price": p.get_price(),
            "stock": p.get_stock(),
        }
        for p in inventory.get_all_products()
    ]
    
    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)
        
    print(f"Inventory successfully saved ({len(data)} products) to inventory.json.")


# ==============================
# MENU & HANDLERS
# ==============================
def handle_add_product(inventory):
    
    print("\n--- Add New Product ---")
    
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

    product = Product(pid, name, price, stock)
    
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

    if product.upate_stock(new_stock):
        
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
            
        elif choice == "0":
            numofrecords = len(inventory.get_all_products())
            print("Goodbye!")
            print(f"Total Records in JSON: {numofrecords}")
            break
        
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()