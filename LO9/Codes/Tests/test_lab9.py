import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Inventory import Inventory
from filehandling import load_products
from Models.product import Product
from Models.order import Order
from Models.order_line import OrderLine
from Models.supplier import Supplier
from Models.product_factory import ProductFactory
from Models.discount_strategy import (
    BulkDiscount,
    PercentageDiscount,
    NoDiscount,
)


class Lab9Tests(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S1", "Supplier", "supplier@example.com")

    def test_product_factory_creates_physical_product(self):
        product = ProductFactory.create(
            "physical", "P1", "Lamp", 25.0, 10, self.supplier, weight=1.2
        )
        self.assertEqual(product.get_product_id(), "P1")
        self.assertIsInstance(product, Product)

    def test_unknown_product_type_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type"):
            ProductFactory.create(
                "service", "S1", "Install", 30.0, 5, self.supplier
            )

    def test_bulk_and_percentage_discount(self):
        product = ProductFactory.create(
            "physical", "P1", "Lamp", 125.0, 10, self.supplier, weight=1
        )
        order = Order("O1", BulkDiscount(200, 20))
        order.add_order_line(product, 2)
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_no_discount_is_default(self):
        order = Order("O1")
        product = ProductFactory.create(
            "digital", "D1", "Editor", 49.9, 100, self.supplier,
            download_size=850
        )
        order.add_order_line(product, 1)
        self.assertEqual(order.calculate_total(), 49.9)

    def test_invalid_price_stock_and_quantity_raise_value_error(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "physical", "P1", "Lamp", 0, 10, self.supplier, weight=1
            )
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "digital", "D1", "Editor", 10, -1, self.supplier,
                download_size=50
            )
        product = ProductFactory.create(
            "digital", "D1", "Editor", 10, 1, self.supplier,
            download_size=50
        )
        with self.assertRaises(ValueError):
            OrderLine(product, 0)

    def test_load_products_skips_bad_rows_and_loads_valid_rows(self):
        inventory = Inventory()
        csv_path = os.path.join(os.path.dirname(__file__), "..", "products.csv")
        load_products(csv_path, inventory, self.supplier)
        ids = {product.get_product_id() for product in inventory.get_all_products()}
        self.assertIn("P001", ids)
        self.assertIn("D001", ids)
        self.assertIn("P003", ids)
        self.assertNotIn("S001", ids)
        self.assertNotIn("P002", ids)

    def test_missing_file_is_handled(self):
        inventory = Inventory()
        load_products("missing-products.csv", inventory, self.supplier)
        self.assertEqual(inventory.get_all_products(), [])


if __name__ == "__main__":
    unittest.main()
