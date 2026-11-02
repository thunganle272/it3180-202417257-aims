import io
import unittest
from contextlib import redirect_stdout

from aims.cart import MAX_NUMBERS_ORDERED, Cart
from aims.dvd import DigitalVideoDisc


class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()

    def add(self, dvd):
        with redirect_stdout(io.StringIO()):
            return self.cart.add_dvd(dvd)

    def test_add_dvd_until_full(self):
        for i in range(MAX_NUMBERS_ORDERED):
            self.assertTrue(self.add(DigitalVideoDisc(f"DVD {i}", cost=1.0)))
        self.assertFalse(self.add(DigitalVideoDisc("DVD 21", cost=1.0)))
        self.assertEqual(len(self.cart.items), MAX_NUMBERS_ORDERED)

    def test_total_cost(self):
        self.add(DigitalVideoDisc("The Lion King", cost=19.95))
        self.add(DigitalVideoDisc("Star Wars", cost=24.95))
        self.add(DigitalVideoDisc("Aladdin", cost=18.99))
        self.assertAlmostEqual(self.cart.total_cost(), 63.89)


if __name__ == "__main__":
    unittest.main()
