import unittest
from datetime import date

from src.domain.client import Client
from src.domain.movie import Movie
from src.repository.client_repository import ClientRepository
from src.repository.movie_repository import MovieRepository
from src.repository.rental_repository import RentalRepository
from src.services.rental_service import RentalService
from src.validators.exceptions import ServiceException
from src.validators.rental_validator import RentalValidator


class TestRentalService(unittest.TestCase):

    def test_add(self):
        movie_repo = MovieRepository()
        movie_repo.add(Movie(3665, 'Avatar', 'About wonderful creatures', 'SF'))

        client_repo = ClientRepository()
        client_repo.add(Client(103, 'Uriesu Iulius'))

        rental_repo = RentalRepository()
        rental_validator = RentalValidator()

        rental_service = RentalService(movie_repo, client_repo, rental_repo, rental_validator)
        self.assertEqual(rental_service.size(), 0)

        rental_id = 901
        movie_id = 3665
        client_id = 103
        rented_date = date(2022, 12, 3)
        due_date = date(2022, 12, 9)
        returned_date = None

        rental_service.add(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
        self.assertEqual(rental_service.size(), 1)

        rental_id = 902
        movie_id = 3665
        client_id = 103
        rented_date = date(2022, 12, 15)
        due_date = date(2022, 12, 20)
        returned_date = None

        try:
            rental_service.add(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
            assert False
        except ServiceException as se:
            self.assertEqual(str(se), 'Client has movies that passed their due date for return!')
