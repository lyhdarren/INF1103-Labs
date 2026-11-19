from Models.product import Product
from Models.supplier import Supplier
from Models.physical_product import PhysicalProduct
from Models.digital_product import DigitalProduct


class ProductFactory:

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        **details
    ) -> Product:
        product_type = product_type.strip().lower()

        if product_type == "physical":
            return PhysicalProduct(
                product_id,
                name,
                price,
                stock_quantity,
                supplier,
                details.get("weight", 0.0)
            )

        if product_type == "digital":
            return DigitalProduct(
                product_id,
                name,
                price,
                stock_quantity,
                supplier,
                details.get("download_size", 0.0)
            )

        raise ValueError(f"Unknown product type: {product_type}")
