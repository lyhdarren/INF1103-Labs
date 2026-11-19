from .product import Product, CanBeShipped
from Models.supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weightkg: float
    ):
        super().__init__(
            product_id,
            name,
            price,
            stock,
            supplier
        )

        self.__weightkg = float(weightkg)

    def get_weight(self) -> float:
        return self.__weightkg

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Physical | Weight: {self.get_weight()} kg")
        
        print("\n--- Supplier Information ---")
        self.supplier.display_information()

    def get_fulfillment_info(self) -> str:
        return f"Requires physical shipping ({self.get_weight()} kg)."

    def calculate_shipping_cost(self) -> float:
        return round(5.0 + (2.0 * self.get_weight()), 2)