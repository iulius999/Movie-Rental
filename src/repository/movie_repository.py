from src.domain.movie import Movie
from src.validators.exceptions import RepositoryException


class MovieRepository:

    def __init__(self):
        self._data = {}

    def add(self, movie: Movie):
        if movie.movie_id in self._data.keys():
            raise RepositoryException('A movie already has id ' + str(movie.movie_id) + '!')

        self._data[movie.movie_id] = movie

    def remove(self, movie_id: int):
        self._check_existence(movie_id)
        self._data.pop(movie_id)

    def update_title(self, movie_id: int, new_title: str):
        self._check_existence(movie_id)
        self._data[movie_id].title = new_title

    def update_description(self, movie_id: int, new_description: str):
        self._check_existence(movie_id)
        self._data[movie_id].description = new_description

    def update_genre(self, movie_id: int, new_genre: str):
        self._check_existence(movie_id)
        self._data[movie_id].genre = new_genre

    def get_by_id(self, movie_id: int):
        self._check_existence(movie_id)
        return self._data[movie_id]

    def get_all(self):
        return list(self._data.values())

    def __len__(self):
        return len(self._data)

    def _check_existence(self, movie_id: int):
        if movie_id not in self._data.keys():
            raise RepositoryException('No movie with id ' + str(movie_id) + '!')
