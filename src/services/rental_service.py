from datetime import date

from src.domain.client import Client
from src.domain.movie import Movie
from src.domain.rental import Rental
from src.repository.client_repository import ClientRepository
from src.repository.movie_repository import MovieRepository
from src.repository.rental_repository import RentalRepository
from src.services.undo_service import UndoService, Function, Operation
from src.validators.exceptions import ServiceException
from src.validators.rental_validator import RentalValidator


class MovieRentalDTO:

    def __init__(self, movie: Movie, rented_days: int):
        self._movie = movie
        self._rented_days = rented_days

    @property
    def movie(self):
        return self._movie

    @property
    def rented_days(self):
        return self._rented_days

    @rented_days.setter
    def rented_days(self, new_rented_days):
        self._rented_days = new_rented_days

    def __str__(self):
        return str(self.movie) + 'Rented for ' + str(self.rented_days) + ' days\n'


class ClientRentDTO:

    def __init__(self, client: Client, active_days: int):
        self._client = client
        self._active_days = active_days

    @property
    def client(self):
        return self._client

    @property
    def active_days(self):
        return self._active_days

    @active_days.setter
    def active_days(self, new_active_days):
        self._active_days = new_active_days

    def __str__(self):
        return str(self.client) + ' has movies rented for ' + str(self.active_days) + ' days'


class LateRentalDTO:

    def __init__(self, rental: Rental, delay_days: int):
        self._rental = rental
        self._delay_days = delay_days

    @property
    def rental(self):
        return self._rental

    @property
    def delay_days(self):
        return self._delay_days

    def __str__(self):
        return str(self.rental) + 'Delay days: ' + str(self.delay_days) + '\n'


class RentalService:

    def __init__(self, movie_repo: MovieRepository, client_repo: ClientRepository, rental_repo: RentalRepository,
                 rental_validator: RentalValidator, undo_service: UndoService):
        self._movie_repo = movie_repo
        self._client_repo = client_repo
        self._rental_repo = rental_repo
        self._rental_validator = rental_validator
        self._undo_service = undo_service

    def add(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        # 1. Build the object
        rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)

        # 2. Validate it
        self._rental_validator.validate(rental)
        self._movie_repo.get_by_id(movie_id)
        self._client_repo.get_by_id(client_id)

        if not self.can_rent(client_id, rented_date):
            raise ServiceException('Client has movies that passed their due date for return!')

        # 3. Store it
        self._rental_repo.add(rental)

        # Undo means remove
        functions = [Function(self.remove, rental_id)]

        undo = Operation(functions)
        self._undo_service.push(undo)

    def remove(self, rental_id):
        if rental_id < 100:
            raise ServiceException('Rental ID should have at least 3 digits!')

        rental = self._rental_repo.get_by_id(rental_id)
        self._rental_repo.remove(rental_id)

        # Undo means add
        functions = [Function(self.add, rental.rental_id, rental.movie_id, rental.client_id, rental.rented_date,
                              rental.due_date, rental.returned_date)]

        undo = Operation(functions)
        self._undo_service.push(undo)

    def update_returned_date(self, rental_id, new_returned_date):
        if rental_id < 100:
            raise ServiceException('Rental ID should have at least 3 digits!')

        self._rental_repo.update_returned_date(rental_id, new_returned_date)

    def get_all(self):
        return self._rental_repo.get_all()

    def get_by_id(self, rental_id):
        return self._rental_repo.get_by_id(rental_id)

    def rentals_for_client(self, client_id):
        if client_id < 100:
            raise ServiceException('Client ID should have at least 3 digits!')

        self._client_repo.get_by_id(client_id)

        rentals = []
        for rental in self._rental_repo.get_all():
            if rental.client_id == client_id:
                rentals.append(rental.rental_id)

        return rentals

    def passed_due_date(self, rental_id, today: date):
        if rental_id < 100:
            raise ServiceException('Rental ID should have at least 3 digits!')

        rental = self._rental_repo.get_by_id(rental_id)

        if rental.returned_date is not None:
            if rental.returned_date > rental.due_date:
                return True
            return False

        if today > rental.due_date:
            return True
        return False

    def can_rent(self, client_id, today: date):
        if client_id < 100:
            raise ServiceException('Client ID should have at least 3 digits!')

        rentals = self.rentals_for_client(client_id)

        for rental_id in rentals:
            if self.passed_due_date(rental_id, today):
                return False
        return True

    def rentals_of_movie(self, movie_id):
        if movie_id < 100:
            raise ServiceException('Movie ID should have at least 3 digits!')

        self._movie_repo.get_by_id(movie_id)

        rentals = []
        for rental in self._rental_repo.get_all():
            if rental.movie_id == movie_id:
                rentals.append(rental.rental_id)

        return rentals

    def remove_movie(self, movie_id):
        if movie_id < 100:
            raise ServiceException('Movie ID should have at least 3 digits!')

        rentals = self.rentals_of_movie(movie_id)
        for rental_id in rentals:
            self._rental_repo.remove(rental_id)

    def remove_client(self, client_id):
        if client_id < 100:
            raise ServiceException('Client ID should have at least 3 digits!')

        rentals = self.rentals_for_client(client_id)
        for rental_id in rentals:
            self._rental_repo.remove(rental_id)

    # Statistics
    def most_rented_movies(self):
        # Add movies that have no recorded rentals
        # Keys are movie IDs, values are DTO instances
        # DTO = Data Transfer Object
        dto = {}
        for rental in self._rental_repo.get_all():
            if rental.movie_id not in dto.keys():
                dto[rental.movie_id] = MovieRentalDTO(self._movie_repo.get_by_id(rental.movie_id), len(rental))
            else:
                dto[rental.movie_id].rented_days += len(rental)

        for movie in self._movie_repo.get_all():
            if movie.movie_id not in dto.keys():
                dto[movie.movie_id] = MovieRentalDTO(movie, 0)

        results = list(dto.values())
        results.sort(key=lambda x: x.rented_days, reverse=True)
        return results

    def most_active_clients(self):
        # Add clients that have no recorded rentals
        # Keys are client IDs, values are DTO instances
        # DTO = Data Transfer Object
        dto = {}
        for rental in self._rental_repo.get_all():
            if rental.client_id not in dto.keys():
                dto[rental.client_id] = ClientRentDTO(self._client_repo.get_by_id(rental.client_id), len(rental))
            else:
                dto[rental.client_id].active_days += len(rental)

        for client in self._client_repo.get_all():
            if client.client_id not in dto.keys():
                dto[client.client_id] = ClientRentDTO(client, 0)

        results = list(dto.values())
        results.sort(key=lambda x: x.active_days, reverse=True)
        return results

    def late_rentals(self, today: date):
        # Keys are rental IDs, values are DTO instances
        # DTO = Data Transfer Object
        dto = {}
        for rental in self._rental_repo.get_all():
            if rental.returned_date is None and today > rental.due_date:
                dto[rental.rental_id] = LateRentalDTO(rental, (today - rental.due_date).days)
            elif rental.returned_date is not None and rental.returned_date > rental.due_date:
                dto[rental.rental_id] = LateRentalDTO(rental, (rental.returned_date - rental.due_date).days)

        results = list(dto.values())
        results.sort(key=lambda x: x.delay_days, reverse=True)
        return results

    def size(self):
        return len(self._rental_repo)
