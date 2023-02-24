from src.domain.client import Client
from src.validators.exceptions import ClientValidationException


class ClientValidator:

    @staticmethod
    def validate(client: Client):
        errors = []

        if client.client_id < 100:
            errors.append('Client ID should have at least 3 digits!')
        if len(client.name) < 3:
            errors.append('Client name should have at least 3 letters!')

        if len(errors) > 0:
            raise ClientValidationException(errors)
