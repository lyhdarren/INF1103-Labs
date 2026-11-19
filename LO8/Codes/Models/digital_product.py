from .product import Product
from Models.supplier import Supplier


class DigitalProduct(Product):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float
    ):
        super().__init__(
            product_id,
            name,
            price,
            stock,
            supplier
        )

        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Digital | Download Size: {self.__download_size} MB")

    def get_fulfillment_info(self) -> str:
        return f"Digital download ({self.__download_size} MB)."