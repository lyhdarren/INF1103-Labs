import json
from Models.physical_product import PhysicalProduct
from Models.digital_product import DigitalProduct
from Models.supplier import Supplier


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
                    product = PhysicalProduct(
                        pid,
                        name,
                        price,
                        stock,
                        supplier,
                        float(row["weight"])
                    )

                elif ptype == "digital":
                    product = DigitalProduct(
                        pid,
                        name,
                        price,
                        stock,
                        supplier,
                        float(row["download_size"])
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