from .product import Product, CanBeShipped
from .physical_product import PhysicalProduct
from .digital_product import DigitalProduct
from .discount_strategy import (
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)
from .product_factory import ProductFactory

__all__ = [
    "Product",
    "CanBeShipped",
    "PhysicalProduct",
    "DigitalProduct",
    "DiscountStrategy",
    "NoDiscount",
    "PercentageDiscount",
    "BulkDiscount",
    "StudentDiscount",
    "ProductFactory",
]