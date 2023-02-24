from src.domain.client import Client
from src.domain.movie import Movie
from src.domain.rental import Rental
from src.repository.client_repository import ClientRepository
from src.repository.movie_repository import MovieRepository
from src.repository.rental_repository import RentalRepository
from src.services.client_service import ClientService
from src.services.movie_service import MovieService
from src.services.rental_service import RentalService
from src.services.undo_service import UndoService
from src.ui.ui import UI
from src.validators.client_validator import ClientValidator
from src.validators.movie_validator import MovieValidator
from src.validators.rental_validator import RentalValidator
import random
from datetime import date


def generate_movies():
    movies = list()

    movies.append(Movie(3665, 'Avatar', 'About wonderful creatures', 'SF'))
    movies.append(Movie(2399, 'Fast and Furious', 'About fast cars', 'Action'))
    movies.append(Movie(8337, 'Pirates of the Caribbean', 'About pirates', 'Adventure'))
    movies.append(Movie(6640, 'The Conjuring', 'About ghosts and demons', 'Horror'))
    movies.append(Movie(8812, 'Interstellar', 'About space and time travelling', 'SF'))

    return movies


def generate_clients():
    clients = list()

    clients.append(Client(103, 'Uriesu Iulius'))
    clients.append(Client(104, 'Uzum Razvan'))
    clients.append(Client(105, 'Pop Dorian'))
    clients.append(Client(106, 'Zgarcea Robert'))
    clients.append(Client(107, 'Tripon David'))

    return clients


def generate_rentals(n: int):
    rentals = []

    rental_id = 901
    for i in range(n):
        movie_id = random.choice([3665, 2399, 8337, 6640, 8812])
        client_id = random.randint(103, 107)

        rent_year = 2022
        rent_month = random.randint(1, 6)
        rent_day = random.randint(1, 28)
        rent_date = date(rent_year, rent_month, rent_day)

        due_year = 2022
        due_month = random.randint(7, 12)
        due_day = random.randint(1, 30)
        due_date = date(due_year, due_month, due_day)

        r = Rental(rental_id, movie_id, client_id, rent_date, due_date, None)
        rentals.append(r)

        rental_id += 1

    return rentals


if __name__ == '__main__':
    movie_repo = MovieRepository()
    # movie_list = generate_movies()
    # for movie in movie_list:
    #     movie_repo.add(movie)

    client_repo = ClientRepository()
    # client_list = generate_clients()
    # for client in client_list:
    #     client_repo.add(client)

    rental_repo = RentalRepository()
    # rental_list = generate_rentals(20)
    # for rental in rental_list:
    #     rental_repo.add(rental)

    movie_validator = MovieValidator()
    client_validator = ClientValidator()
    rental_validator = RentalValidator()

    undo_service = UndoService()
    rental_service = RentalService(movie_repo, client_repo, rental_repo, rental_validator, undo_service)
    movie_service = MovieService(movie_repo, movie_validator, undo_service, rental_service)
    client_service = ClientService(client_repo, client_validator, undo_service)

    ui = UI(movie_service, client_service, rental_service, undo_service)
    ui.start()
