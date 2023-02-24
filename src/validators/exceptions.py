class ValidationException(Exception):

    def __init__(self, errors):
        self._errors = errors

    def __str__(self):
        result = ''
        for error in self._errors:
            result += error + '\n'

        return result


class MovieValidationException(ValidationException):
    pass


class ClientValidationException(ValidationException):
    pass


class RentalValidationException(ValidationException):
    pass


class RepositoryException(Exception):
    pass


class ServiceException(Exception):
    pass


class UndoException(Exception):
    pass
