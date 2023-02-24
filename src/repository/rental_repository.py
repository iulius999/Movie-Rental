from datetime import date
from src.domain.rental import Rental
from src.validators.exceptions import RepositoryException


class RentalRepository:

    def __init__(self):
        self._data = {}

    def add(self, rental: Rental):
        if rental.rental_id in self._data.keys():
            raise RepositoryException('A rental already has id ' + str(rental.rental_id) + '!')

        self._data[rental.rental_id] = rental

    def remove(self, rental_id: int):
        self._check_existence(rental_id)
        self._data.pop(rental_id)

    def update_returned_date(self, rental_id: int, new_returned_date: date):
        self._check_existence(rental_id)
        self._data[rental_id].returned_date = new_returned_date

    def get_by_id(self, rental_id: int):
        self._check_existence(rental_id)
        return self._data[rental_id]

    def get_all(self):
        return list(self._data.values())

    def __len__(self):
        return len(self._data)

    def _check_existence(self, rental_id: int):
        if rental_id not in self._data.keys():
            raise RepositoryException('No rental with id ' + str(rental_id) + '!')
