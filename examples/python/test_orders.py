"""Behaviour tests. The same file runs against every version of orders.py."""
import importlib.util
import os
import unittest

VERSION = os.environ.get("ORDERS_VERSION", "before")
_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), VERSION, "orders.py")
_spec = importlib.util.spec_from_file_location("orders", _path)
orders = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orders)

ITEMS = [
    {"price": 19.99, "quantity": 3},
    {"price": 0.1, "quantity": 7},
    {"price": 5.25, "quantity": 1},
]


class TotalTests(unittest.TestCase):
    def test_total_with_tax(self):
        self.assertEqual(orders.calculate_order_total(ITEMS, 0.14), 75.15)

    def test_empty_order(self):
        self.assertEqual(orders.calculate_order_total([], 0.14), 0)

    def test_cart_total_is_still_public_and_equal(self):
        self.assertEqual(
            orders.calculate_cart_total(ITEMS, 0.14),
            orders.calculate_order_total(ITEMS, 0.14),
        )


class DiscountTests(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual(orders.get_discount({"tier": "gold"}), 0.1)
        self.assertEqual(orders.get_discount({"tier": "silver"}), 0.05)
        self.assertEqual(orders.get_discount({"tier": "bronze"}), 0)

    def test_missing_customer_or_tier(self):
        self.assertEqual(orders.get_discount(None), 0)
        self.assertEqual(orders.get_discount({}), 0)

    def test_unhashable_tier_does_not_raise(self):
        self.assertEqual(orders.get_discount({"tier": ["gold"]}), 0)


class SummaryTests(unittest.TestCase):
    def test_summary(self):
        self.assertEqual(
            orders.summarize(ITEMS, 0.14, {"tier": "gold"}),
            {"total": "$67.64", "units": 11, "bulk": True},
        )

    def test_summary_without_customer(self):
        self.assertEqual(
            orders.summarize(ITEMS[:1], 0, None),
            {"total": "$59.97", "units": 3, "bulk": False},
        )

    def test_bulk_boundary(self):
        self.assertFalse(orders.is_bulk_order([{"price": 1, "quantity": 9}]))
        self.assertTrue(orders.is_bulk_order([{"price": 1, "quantity": 10}]))
        self.assertIs(orders.is_bulk_order([]), False)

    def test_format_price(self):
        self.assertEqual(orders.format_price(5), "$5.00")
        self.assertEqual(orders.format_price(1234.5), "$1234.50")


if __name__ == "__main__":
    unittest.main()
