import unittest
from datetime import date

from src.domain.rental import Rental
from src.repository.rental_repository import RentalRepository


class TestRentalRepository(unittest.TestCase):

    def test_add(self):
        rental_repo = RentalRepository()
        self.assertEqual(len(rental_repo), 0)

        r1 = Rental(901, 3665, 103, date(2022, 12, 3), date(2022, 12, 9), None)
        rental_repo.add(r1)
        self.assertEqual(len(rental_repo), 1)

        r2 = Rental(902, 2399, 104, date(2022, 12, 7), date(2022, 12, 20), None)
        rental_repo.add(r2)
        self.assertEqual(len(rental_repo), 2)
