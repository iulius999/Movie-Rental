from src.domain.movie import Movie
from src.repository.movie_repository import MovieRepository
from src.services.rental_service import RentalService
from src.services.undo_service import UndoService, Function, Operation
from src.validators.exceptions import ServiceException
from src.validators.movie_validator import MovieValidator


class MovieService:

    def __init__(self, movie_repo: MovieRepository, movie_validator: MovieValidator, undo_service: UndoService,
                 rental_service: RentalService):
        self._movie_repo = movie_repo
        self._movie_validator = movie_validator
        self._undo_service = undo_service
        self._rental_service = rental_service

    def add(self, movie_id, title, description, genre):
        # 1. Build the object
        movie = Movie(movie_id, title, description, genre)

        # 2. Validate it
        self._movie_validator.validate(movie)

        # 3. Store it
        self._movie_repo.add(movie)

        # Undo means remove
        functions = [Function(self.remove, movie_id)]

        undo = Operation(functions)
        self._undo_service.push(undo)

    def remove(self, movie_id):
        if movie_id < 100:
            raise ServiceException('Movie ID should have at least 3 digits!')

        movie = self._movie_repo.get_by_id(movie_id)
        rentals = self._rental_service.rentals_of_movie(movie_id)

        # Undo means add
        functions = [Function(self.add, movie.movie_id, movie.title, movie.description, movie.genre)]

        self._movie_repo.remove(movie_id)
        # Also, remove all the rentals having that movie
        for rental_id in rentals:
            rental = self._rental_service.get_by_id(rental_id)
            self._rental_service.remove(rental.rental_id)
            functions.append(Function(self._rental_service.add, rental.rental_id, rental.movie_id, rental.client_id,
                                      rental.rented_date, rental.due_date, rental.returned_date))

        undo = Operation(functions)
        self._undo_service.push(undo)

    def update_title(self, movie_id, new_title):
        if movie_id < 100:
            raise ServiceException('Movie ID should have at least 3 digits!')

        if len(new_title) < 3:
            raise ServiceException('Movie title should have at least 3 letters!')

        self._movie_repo.update_title(movie_id, new_title)

    def update_description(self, movie_id, new_description):
        if movie_id < 100:
            raise ServiceException('Movie ID should have at least 3 digits!')

        if len(new_description) < 5:
            raise ServiceException('Movie description should have at least 5 letters!')

        self._movie_repo.update_description(movie_id, new_description)

    def update_genre(self, movie_id, new_genre):
        if movie_id < 100:
            raise ServiceException('Movie ID should have at least 3 digits!')

        if len(new_genre) < 2:
            raise ServiceException('Movie genre should have at least 2 letters!')

        self._movie_repo.update_genre(movie_id, new_genre)

    def get_by_id(self, movie_id):
        if movie_id < 100:
            raise ServiceException('Movie ID should have at least 3 digits!')

        return self._movie_repo.get_by_id(movie_id)

    def get_all(self):
        return self._movie_repo.get_all()

    def search(self, something):
        something = something.lower()
        found_movies = []

        for movie in self._movie_repo.get_all():
            if str(movie.movie_id).lower().find(something) != -1 or movie.title.lower().find(something) != -1 or \
               movie.description.lower().find(something) != -1 or movie.genre.lower().find(something) != -1:
                found_movies.append(movie)

        return found_movies

    def size(self):
        return len(self._movie_repo)
