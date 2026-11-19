import json
import csv
from Models.physical_product import PhysicalProduct
from Models.digital_product import DigitalProduct
from Models.supplier import Supplier
from Models.product_factory import ProductFactory


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            rows = csv.DictReader(file)
            for row in rows:
                try:
                    price = float(row["price"])
                    stock = int(row["stock_quantity"])
                    details = {}
                    product_type = row["product_type"]
                    if product_type == "physical":
                        if row.get("weight"):
                            details["weight"] = float(row["weight"])
                    elif product_type == "digital":
                        if row.get("download_size"):
                            details["download_size"] = float(row["download_size"])

                    product = ProductFactory.create(
                        product_type,
                        row["product_id"],
                        row["name"],
                        price,
                        stock,
                        supplier,
                        **details
                    )
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Skipping duplicate product ID: {row['product_id']}")
                except (KeyError, TypeError, ValueError) as error:
                    print(
                        f"Skipping invalid row {row.get('product_id', 'unknown')}: "
                        f"{error}"
                    )
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


class FileHandling:
    def __init__(self, filename="inventory.json"):
        self.filename = filename

    def load_inventory(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError:
            print(f"{self.filename} not found — starting with an empty inventory.")
            return []

        except json.JSONDecodeError as e:
            print(f"{self.filename} is corrupted — starting with an empty inventory.")
            print(f"JSON error: {e}")
            return []

        products = []

        for row in data:
            try:
                # Basic product information
                ptype = row["type"]
                pid = str(row["product_id"]).strip()
                name = str(row["name"]).strip()
                price = float(row["price"])
                stock = int(row["stock_quantity"])

                # Supplier information
                supplier_data = row["supplier"]

                supplier = Supplier(
                    supplier_id=str(supplier_data["supplier_id"]).strip(),
                    name=str(supplier_data["name"]).strip(),
                    contact_email=str(
                        supplier_data["contact_email"]
                    ).strip()
                )

                # Create the correct Product subclass
                if ptype == "physical":
                    product = ProductFactory.create(
                        "physical",
                        pid,
                        name,
                        price,
                        stock,
                        supplier,
                        weight=float(row["weight"])
                    )

                elif ptype == "digital":
                    product = ProductFactory.create(
                        "digital",
                        pid,
                        name,
                        price,
                        stock,
                        supplier,
                        download_size=float(row["download_size"])
                    )

                else:
                    print(f"Skipping unknown product type: {ptype}")
                    continue

                products.append(product)

            except (KeyError, ValueError, TypeError) as e:
                print(f"Skipping bad record: {row} ({e})")

        return products

    def save_inventory(self, inventory):
        data = []

        for p in inventory.get_all_products():

            base = {
                "product_id": p.get_product_id(),
                "name": p.get_name(),
                "price": p.get_price(),
                "stock_quantity": p.get_stock(),
            }

            # Save supplier information
            supplier = p.get_supplier()
            base["supplier"] = {
                "supplier_id": supplier.get_supplier_id(),
                "name": supplier.get_name(),
                "contact_email": supplier.get_contact_email()
            }

            # Physical product
            if isinstance(p, PhysicalProduct):
                base["type"] = "physical"
                base["weight"] = p.get_weight()

            # Digital product
            elif isinstance(p, DigitalProduct):
                base["type"] = "digital"
                base["download_size"] = p.get_download_size()

            data.append(base)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(
            f"Inventory successfully saved "
            f"({len(data)} products) to {self.filename}."
        )