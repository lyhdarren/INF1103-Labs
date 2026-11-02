import json
from Models.physical_product import PhysicalProduct
from Models.digital_product import DigitalProduct


class FileHandling:
    def __init__(self, filename="inventory.json"):
        self.filename = filename

    def load_inventory(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"{self.filename} not found — starting with an empty inventory.")
            return []
        except json.JSONDecodeError:
            print(f"{self.filename} is corrupted — starting with an empty inventory.")
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

    def save_inventory(self, inventory):
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

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory successfully saved ({len(data)} products) to {self.filename}.")