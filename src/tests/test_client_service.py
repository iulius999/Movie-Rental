import unittest

from src.repository.client_repository import ClientRepository
from src.services.client_service import ClientService
from src.validators.client_validator import ClientValidator
from src.validators.exceptions import ServiceException, ClientValidationException


class TestClientService(unittest.TestCase):

    def test_add(self):
        client_repo = ClientRepository()
        client_validator = ClientValidator()
        client_service = ClientService(client_repo, client_validator)
        self.assertEqual(client_service.size(), 0)

        client_id = 103
        name = 'Uriesu Iulius'

        client_service.add(client_id, name)
        self.assertEqual(client_service.size(), 1)

        try:
            client_id = 99
            name = 'ab'
            client_service.add(client_id, name)
            self.assert_(False)

        except ClientValidationException as cve:
            error = 'Client ID should have at least 3 digits!\n'
            error += 'Client name should have at least 3 letters!\n'
            self.assertEqual(str(cve), error)

    def test_remove(self):
        client_repo = ClientRepository()
        client_validator = ClientValidator()
        client_service = ClientService(client_repo, client_validator)

        client_id = 103
        name = 'Uriesu Iulius'
        client_service.add(client_id, name)

        client_id = 104
        name = 'Uzum Razvan'
        client_service.add(client_id, name)

        client_service.remove(103)
        self.assertEqual(client_service.size(), 1)

        try:
            client_id = 16
            client_service.remove(client_id)
            self.assert_(False)

        except ServiceException as se:
            self.assertEqual(str(se), 'Client ID should have at least 3 digits!')

    def test_get_by_id(self):
        client_repo = ClientRepository()
        client_validator = ClientValidator()
        client_service = ClientService(client_repo, client_validator)

        client_id = 103
        name = 'Uriesu Iulius'
        client_service.add(client_id, name)

        client_id = 105
        name = 'Pop Dorian'
        client_service.add(client_id, name)

        self.assertEqual(client_service.get_by_id(103).name, 'Uriesu Iulius')
        self.assertEqual(client_service.get_by_id(105).name, 'Pop Dorian')

        try:
            client_id = 12
            c = client_service.get_by_id(client_id)
            self.assert_(False)

        except ServiceException as se:
            self.assertEqual(str(se), 'Client ID should have at least 3 digits!')

    def test_update(self):
        client_repo = ClientRepository()
        client_validator = ClientValidator()
        client_service = ClientService(client_repo, client_validator)

        client_id = 103
        name = 'Uriesu Iulius'
        client_service.add(client_id, name)

        client_service.update_name(103, 'Uriesu David')
        self.assertEqual(client_service.get_by_id(103).name, 'Uriesu David')

        try:
            name = 'AB'
            client_service.update_name(client_id, name)
            self.assert_(False)

        except ServiceException as se:
            self.assertEqual(str(se), 'Client name should have at least 3 letters!')
