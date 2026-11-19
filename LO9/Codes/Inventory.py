from Models.product import Product, CanBeShipped


class Inventory:

    def __init__(self):
        # Aggregation:
        # Inventory stores references to Product objects.
        # The Product objects can exist independently of Inventory.
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add a product to the inventory if it does not already exist."""
        if self.search_product(product.get_product_id()) is not None:
            print(
                f"Product ID '{product.get_product_id()}' "
                f"already exists."
            )
            return False

        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove a product from the inventory by product ID."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                self.__products.remove(product)
                return True

        print(f"{product_id} not found!")
        return False

    def search_product(self, product_id: str) -> Product | None:
        """Find and return a product by ID."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def find_product(self, product_id: str) -> Product | None:
        """
        Lab 8 method name.

        Searches for a product by ID and returns the Product
        object if found, otherwise None.
        """
        return self.search_product(product_id)

    def display_all(self) -> None:
        """Display information for all products."""
        if not self.__products:
            print("Inventory Empty")
            return

        for product in self.__products:
            product.display_information()
            print(f"Fulfillment: {product.get_fulfillment_info()}")
            print()

    def display_all_products(self) -> None:
        """Alias for display_all()."""
        self.display_all()

    def get_all_products(self) -> list[Product]:
        """
        Return a copy of the product list.

        The Inventory keeps ownership of its list, but the Product
        objects themselves can exist independently.
        """
        return list(self.__products)

    def total_shipping_cost(self) -> float:
        """Calculate the total shipping cost for shippable products."""
        total: float = 0.0

        for product in self.__products:
            if isinstance(product, CanBeShipped):
                total += product.calculate_shipping_cost()

        return round(total, 2)