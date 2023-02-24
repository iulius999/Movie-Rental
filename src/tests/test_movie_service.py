import copy
import unittest

from src.domain.movie import Movie
from src.repository.movie_repository import MovieRepository
from src.services.movie_service import MovieService
from src.validators.exceptions import MovieValidationException, ServiceException
from src.validators.movie_validator import MovieValidator


class TestMovieService(unittest.TestCase):

    def test_add(self):
        movie_repo = MovieRepository()
        movie_validator = MovieValidator()
        movie_service = MovieService(movie_repo, movie_validator)
        self.assertEqual(movie_service.size(), 0)

        movie_id = 3665
        title = 'Avatar'
        description = 'About wonderful creatures'
        genre = 'SF'

        movie_service.add(movie_id, title, description, genre)
        self.assertEqual(movie_service.size(), 1)

        try:
            movie_id = 29
            title = 'AB'
            description = 'abc'
            genre = 'F'

            movie_service.add(movie_id, title, description, genre)
            assert False

        except MovieValidationException as mve:
            error = 'Movie ID should have at least 3 digits!\n'
            error += 'Movie title should have at least 3 letters!\n'
            error += 'Movie description should have at least 5 letters!\n'
            error += 'Movie genre should have at least 2 letters!\n'
            self.assertEqual(str(mve), error)

    def test_remove(self):
        movie_repo = MovieRepository()
        movie_validator = MovieValidator()
        movie_service = MovieService(movie_repo, movie_validator)

        movie_id = 3665
        title = 'Avatar'
        description = 'About wonderful creatures'
        genre = 'SF'
        movie_service.add(movie_id, title, description, genre)

        movie_service.remove(3665)
        self.assertEqual(movie_service.size(), 0)

        try:
            movie_id = 29
            movie_service.remove(movie_id)
            assert False

        except ServiceException as se:
            self.assertEqual(str(se), 'Movie ID should have at least 3 digits!')

    def test_get_by_id(self):
        movie_repo = MovieRepository()
        movie_validator = MovieValidator()
        movie_service = MovieService(movie_repo, movie_validator)

        movie_id = 3665
        title = 'Avatar'
        description = 'About wonderful creatures'
        genre = 'SF'
        movie_service.add(movie_id, title, description, genre)

        self.assertEqual(movie_service.get_by_id(3665).title, 'Avatar')
        self.assertEqual(movie_service.get_by_id(3665).description, 'About wonderful creatures')
        self.assertEqual(movie_service.get_by_id(3665).genre, 'SF')
        self.assertEqual(movie_service.get_by_id(3665).movie_id, 3665)

        try:
            movie_id = 44
            m = movie_service.get_by_id(movie_id)
            assert False

        except ServiceException as se:
            self.assertEqual(str(se), 'Movie ID should have at least 3 digits!')

    def test_update(self):
        movie_repo = MovieRepository()
        movie_validator = MovieValidator()
        movie_service = MovieService(movie_repo, movie_validator)

        movie_id = 3665
        title = 'Avatar'
        description = 'About wonderful creatures'
        genre = 'SF'
        movie_service.add(movie_id, title, description, genre)

        movie_service.update_title(3665, 'Fast and Furious')
        self.assertEqual(movie_service.get_by_id(3665).title, 'Fast and Furious')

        movie_service.update_description(3665, 'About fast cars')
        self.assertEqual(movie_service.get_by_id(3665).description, 'About fast cars')

        movie_service.update_genre(3665, 'Action')
        self.assertEqual(movie_service.get_by_id(3665).genre, 'Action')

        try:
            movie_service.update_description(3665, 'abcd')
            assert False

        except ServiceException as se:
            self.assertEqual(str(se), 'Movie description should have at least 5 letters!')
