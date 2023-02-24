from src.domain.rental import Rental
from src.validators.exceptions import RentalValidationException
from datetime import date


class RentalValidator:

    @staticmethod
    def validate(rental: Rental):
        errors = []

        if rental.rental_id < 100:
            errors.append('Rental ID should have at least 3 digits!')
        if rental.movie_id < 100:
            errors.append('Movie ID should have at least 3 digits!')
        if rental.client_id < 100:
            errors.append('Client ID should have at least 3 digits!')
        if rental.due_date is not None and rental.rented_date is not None and rental.due_date < rental.rented_date:
            errors.append('Due date cannot be before rent date!')
        if rental.returned_date is not None and rental.rented_date is not None and \
                rental.returned_date < rental.rented_date:
            errors.append('Return date cannot be before rent date!')
        if rental.due_date is not None and rental.rented_date is not None and rental.due_date == rental.rented_date:
            errors.append('Rental must be at least 1 day!')

        day1 = date(2000, 1, 1)
        if rental.rented_date is not None and rental.rented_date < day1:
            errors.append('Rental must start in the 3rd millennium!')

        if len(errors) > 0:
            raise RentalValidationException(errors)
