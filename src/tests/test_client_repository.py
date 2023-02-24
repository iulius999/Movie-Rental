import unittest

from src.domain.client import Client
from src.repository.client_repository import ClientRepository
from src.validators.exceptions import RepositoryException


class TestClientRepository(unittest.TestCase):

    def test_add(self):
        repo = ClientRepository()
        self.assertEqual(len(repo), 0)

        repo.add(Client(999, 'Uriesu Iulius'))
        self.assertEqual(len(repo), 1)

        repo.add(Client(111, 'Uzum Razvan'))
        self.assertEqual(len(repo), 2)

        try:
            repo.add(Client(999, 'Pop Dorian'))
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'A client already has id 999!')

    def test_remove(self):
        repo = ClientRepository()
        repo.add(Client(103, 'Uriesu Iulius'))
        repo.add(Client(104, 'Uzum Razvan'))
        repo.add(Client(105, 'Pop Dorian'))

        repo.remove(104)
        self.assertEqual(len(repo), 2)

        repo.remove(105)
        self.assertEqual(len(repo), 1)

        try:
            repo.remove(999)
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'No client with id 999!')

    def test_get_by_id(self):
        repo = ClientRepository()
        c1 = Client(103, 'Uriesu Iulius')
        c2 = Client(104, 'Uzum Razvan')
        c3 = Client(105, 'Pop Dorian')

        repo.add(c1)
        repo.add(c2)
        repo.add(c3)

        self.assertEqual(repo.get_by_id(103), c1)
        self.assertEqual(repo.get_by_id(104), c2)
        self.assertEqual(repo.get_by_id(105), c3)

        try:
            c4 = repo.get_by_id(999)
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'No client with id 999!')

    def test_update(self):
        repo = ClientRepository()
        c1 = Client(103, 'Uriesu Iulius')
        c2 = Client(104, 'Uzum Razvan')

        repo.add(c1)
        repo.add(c2)

        repo.update_name(104, 'Uzum Viorel')
        self.assertEqual(repo.get_by_id(104).name, 'Uzum Viorel')

        try:
            repo.update_name(999, 'Uriesu Iulius')
            assert False
        except RepositoryException as re:
            self.assertEqual(str(re), 'No client with id 999!')

    def test_get_all(self):
        repo = ClientRepository()
        c1 = Client(103, 'Uriesu Iulius')
        c2 = Client(104, 'Uzum Razvan')
        c3 = Client(105, 'Pop Dorian')

        repo.add(c2)
        repo.add(c1)
        repo.add(c3)

        self.assertEqual(repo.get_all(), [c2, c1, c3])
