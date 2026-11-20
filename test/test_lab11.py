import os
import tempfile
import unittest

from src.modules.fileHandler import load_products
from src.modules.inventory import Inventory
from src.modules.order import Order
from src.modules.orderline import OrderLine
from src.modules.digitalProduct import DigitalProduct
from src.modules.physicalProduct import PhysicalProduct
from src.modules.supplier import Supplier
from src.payment.bulkDiscount import BulkDiscount
from src.payment.noDiscount import NoDiscount
from src.payment.percentageDiscount import PercentageDiscount
from src.payment.studentDiscount import StudentDiscount
from src.product.productFactory import ProductFactory


class TestLab11(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechDistro Inc.", "orders@techdistro.com")
        self.keyboard = ProductFactory.create(
            "physical", "P01", "Keyboard", 100.0, 10, self.supplier, weight=1.2
        )
        self.ebook = ProductFactory.create(
            "digital", "P02", "Python Guide", 25.0, 50, self.supplier, download_size=15.0
        )

    def test_discount_strategies_and_set_discount(self) -> None:
        order = Order("ORD-01")
        order.add_order_line(self.keyboard, 2)  # $200.00
        self.assertEqual(order.calculate_total(), 200.0)  # NoDiscount

        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 180.0)

        order.set_discount(StudentDiscount())
        self.assertEqual(order.calculate_total(), 160.0)

        order.set_discount(BulkDiscount(200, 30))
        self.assertEqual(order.calculate_total(), 170.0)

        order.set_discount(NoDiscount())
        self.assertEqual(order.calculate_total(), 200.0)

    def test_product_factory(self) -> None:
        self.assertIsInstance(self.keyboard, PhysicalProduct)
        self.assertIsInstance(self.ebook, DigitalProduct)
        with self.assertRaises(ValueError):
            ProductFactory.create("service", "S01", "Install", 30.0, 5, self.supplier)

    def test_product_and_orderline_validation(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P03", "Bad", 0.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P03", "Bad", -10.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P03", "Bad", 10.0, -1, self.supplier)
        with self.assertRaises(ValueError):
            self.keyboard.update_stock(-5)
        with self.assertRaises(ValueError):
            OrderLine(self.keyboard, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.keyboard, -2)

    def test_load_products_csv_and_missing_file(self) -> None:
        csv_content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "products.csv")
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                f.write(csv_content)

            inventory = Inventory()
            load_products(csv_path, inventory, self.supplier)
            self.assertEqual(len(inventory.products), 3)

            missing_inv = Inventory()
            load_products(os.path.join(tmpdir, "missing.csv"), missing_inv, self.supplier)
            self.assertEqual(len(missing_inv.products), 0)


if __name__ == "__main__":
    unittest.main()
