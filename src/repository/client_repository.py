from src.domain.client import Client
from src.validators.exceptions import RepositoryException


class ClientRepository:

    def __init__(self):
        self._data = {}

    def add(self, client: Client):
        if client.client_id in self._data.keys():
            raise RepositoryException('A client already has id ' + str(client.client_id) + '!')

        self._data[client.client_id] = client

    def remove(self, client_id: int):
        self._check_existence(client_id)
        self._data.pop(client_id)

    def update_name(self, client_id: int, new_name: str):
        self._check_existence(client_id)
        self._data[client_id].name = new_name

    def get_by_id(self, client_id: int):
        self._check_existence(client_id)
        return self._data[client_id]

    def get_all(self):
        return list(self._data.values())

    def __len__(self):
        return len(self._data)

    def _check_existence(self, client_id: int):
        if client_id not in self._data.keys():
            raise RepositoryException('No client with id ' + str(client_id) + '!')
