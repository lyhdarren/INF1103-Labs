from Inventory import Inventory
from filehandling import FileHandling
from Models.physical_product import PhysicalProduct
from Models.digital_product import DigitalProduct
from Models.product import CanBeShipped

# ==============================
# MAIN CLASS (CONTROLLER)
# ==============================
class Main:
    def __init__(self):
        self.fh = FileHandling("inventory.json")
        self.inventory = Inventory()
        
        # Load existing data into the inventory
        for product in self.fh.load_inventory():
            self.inventory.add_product(product)

    def handle_add_product(self):
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

        if self.inventory.add_product(product):
            print(f"SUCCESS: Product '{name}' added to memory.")
            self.fh.save_inventory(self.inventory)
        else:
            print(f"FAILED: Product ID '{pid}' already exists.")

    def handle_update_stock(self):
        print("\n--- Update Stock ---")
        pid = input("Enter product ID: ").strip()
        product = self.inventory.search_product(pid)

        if product is None:
            print(f"Error: Product ID {pid} not found!")
            return

        try:
            new_stock = int(input("Enter new stock quantity: "))
        except ValueError:
            print("Invalid quantity. Please enter a whole number.")
            return

        if product.update_stock(new_stock):
            print(f"Stock for {product.get_name()} updated to {new_stock} in memory.")
            self.fh.save_inventory(self.inventory)

    def handle_search(self):
        print("\n--- Search Product ---")
        pid = input("Enter product ID: ").strip()
        product = self.inventory.search_product(pid)

        if product is None:
            print(f"Error: Product ID {pid} not found!")
            return

        print("Product Found:")
        product.display_information()
        print(f"Fulfillment: {product.get_fulfillment_info()}")
        if isinstance(product, CanBeShipped):
            print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")

    def handle_shipping_total(self):
        print(f"\nTotal shipping cost of inventory: ${self.inventory.total_shipping_cost():.2f}")

    def run(self):
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
                self.inventory.display_all()
            elif choice == "2":
                self.handle_add_product()
            elif choice == "3":
                self.handle_update_stock()
            elif choice == "4":
                self.handle_search()
            elif choice == "5":
                self.handle_shipping_total()
            elif choice == "0":
                print("Goodbye!")
                print(f"Total Records in JSON: {len(self.inventory.get_all_products())}")
                break
            else:
                print("Invalid choice. Please enter a number from 0 to 5.")


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    app = Main() 
    app.run()     