import unittest

from src.domain.movie import Movie
from src.repository.movie_repository import MovieRepository
from src.validators.exceptions import RepositoryException


class TestMovieRepository(unittest.TestCase):

    def test_add(self):
        repo = MovieRepository()
        self.assertEqual(len(repo), 0)

        repo.add(Movie(3665, 'Avatar', 'About wonderful creatures', 'SF'))
        self.assertEqual(len(repo), 1)

        repo.add(Movie(2399, 'Fast and Furious 7', 'About super cars', 'Action'))
        self.assertEqual(len(repo), 2)

        try:
            repo.add(Movie(2399, 'Pirates of the Caribbean', 'About pirates', 'Adventure'))
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'A movie already has id 2399!')

    def test_remove(self):
        repo = MovieRepository()
        repo.add(Movie(3665, 'Avatar', 'About wonderful creatures', 'SF'))
        repo.add(Movie(2399, 'Fast and Furious 7', 'About super cars', 'Action'))
        repo.add(Movie(4495, 'Pirates of the Caribbean', 'About pirates', 'Adventure'))

        repo.remove(3665)
        self.assertEqual(len(repo), 2)

        repo.remove(4495)
        self.assertEqual(len(repo), 1)

        try:
            repo.remove(1234)
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'No movie with id 1234!')

    def test_get_by_id(self):
        repo = MovieRepository()
        m1 = Movie(3665, 'Avatar', 'About wonderful creatures', 'SF')
        m2 = Movie(2399, 'Fast and Furious 7', 'About super cars', 'Action')
        m3 = Movie(4495, 'Pirates of the Caribbean', 'About pirates', 'Adventure')

        repo.add(m1)
        repo.add(m2)
        repo.add(m3)

        self.assertEqual(repo.get_by_id(3665), m1)
        self.assertEqual(repo.get_by_id(2399), m2)
        self.assertEqual(repo.get_by_id(4495), m3)

        try:
            m4 = repo.get_by_id(1234)
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'No movie with id 1234!')

    def test_update(self):
        repo = MovieRepository()
        repo.add(Movie(3665, 'Avatar', 'About wonderful creatures', 'SF'))
        repo.add(Movie(2399, 'Fast and Furious 7', 'About super cars', 'Action'))
        repo.add(Movie(4495, 'Pirates of the Caribbean', 'About pirates', 'Adventure'))

        repo.update_title(3665, 'Avatar 2')
        self.assertEqual(repo.get_by_id(3665).title, 'Avatar 2')

        repo.update_description(2399, 'About super cars and family')
        self.assertEqual(repo.get_by_id(2399).description, 'About super cars and family')

        repo.update_genre(4495, 'Action and Adventure')
        self.assertEqual(repo.get_by_id(4495).genre, 'Action and Adventure')

        try:
            repo.update_title(1234, 'The Walk')
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'No movie with id 1234!')

    def test_get_all(self):
        repo = MovieRepository()
        m1 = Movie(7813, 'Avatar', 'About wonderful creatures', 'SF')
        m2 = Movie(2399, 'Fast and Furious 7', 'About super cars', 'Action')
        m3 = Movie(4495, 'Pirates of the Caribbean', 'About pirates', 'Adventure')

        repo.add(m2)
        repo.add(m3)
        repo.add(m1)

        self.assertEqual(repo.get_all(), [m2, m3, m1])
