import io
import unittest
from contextlib import redirect_stdout

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class TestSort(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        with redirect_stdout(io.StringIO()):
            self.cart.add_dvd(DigitalVideoDisc("Star Wars", cost=24.95))
            self.cart.add_dvd(DigitalVideoDisc("Aladdin", cost=18.99))
            self.cart.add_dvd(DigitalVideoDisc("The Lion King", cost=19.95))

    def titles(self):
        return [dvd.title for dvd in self.cart.items]

    def test_sort_by_title(self):
        self.cart.sort_by_title()
        self.assertEqual(self.titles(), ["Aladdin", "Star Wars", "The Lion King"])

    def test_sort_by_cost(self):
        self.cart.sort_by_cost()
        self.assertEqual(self.titles(), ["Star Wars", "The Lion King", "Aladdin"])


if __name__ == "__main__":
    unittest.main()
