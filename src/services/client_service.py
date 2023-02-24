from src.domain.client import Client
from src.repository.client_repository import ClientRepository
from src.services.undo_service import Function, Operation, UndoService
from src.validators.client_validator import ClientValidator
from src.validators.exceptions import ServiceException


class ClientService:

    def __init__(self, client_repo: ClientRepository, client_validator: ClientValidator, undo_service: UndoService):
        self._client_repo = client_repo
        self._client_validator = client_validator
        self._undo_service = undo_service

    def add(self, client_id, name):
        # 1. Build the object
        client = Client(client_id, name)

        # 2. Validate it
        self._client_validator.validate(client)

        # 3. Store it
        self._client_repo.add(client)

        # Undo means remove
        functions = [Function(self.remove, client_id)]

        undo = Operation(functions)
        self._undo_service.push(undo)

    def remove(self, client_id):
        if client_id < 100:
            raise ServiceException('Client ID should have at least 3 digits!')

        client = self._client_repo.get_by_id(client_id)
        self._client_repo.remove(client_id)

        # Undo means add
        functions = [Function(self.add, client.client_id, client.name)]

        undo = Operation(functions)
        self._undo_service.push(undo)

    def update_name(self, client_id, new_name):
        if client_id < 100:
            raise ServiceException('Client ID should have at least 3 digits!')

        if len(new_name) < 3:
            raise ServiceException('Client name should have at least 3 letters!')

        self._client_repo.update_name(client_id, new_name)

    def get_by_id(self, client_id):
        if client_id < 100:
            raise ServiceException('Client ID should have at least 3 digits!')

        return self._client_repo.get_by_id(client_id)

    def get_all(self):
        return self._client_repo.get_all()

    def search(self, something):
        something = something.lower()
        found_clients = []

        for client in self._client_repo.get_all():
            if str(client.client_id).lower().find(something) != -1 or client.name.lower().find(something) != -1:
                found_clients.append(client)

        return found_clients

    def size(self):
        return len(self._client_repo)
