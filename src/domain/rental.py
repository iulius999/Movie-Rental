from datetime import date


class Rental:

    def __init__(self, rental_id: int, movie_id: int, client_id: int, rented_date: date, due_date: date,
                 returned_date):
        self._rental_id = rental_id
        self._movie_id = movie_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._due_date = due_date
        self._returned_date = returned_date

    @property
    def rental_id(self):
        return self._rental_id

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def client_id(self):
        return self._client_id

    @property
    def rented_date(self):
        return self._rented_date

    @rented_date.setter
    def rented_date(self, new_rented_date):
        self._rented_date = new_rented_date

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, new_due_date):
        self._due_date = new_due_date

    @property
    def returned_date(self):
        return self._returned_date

    @returned_date.setter
    def returned_date(self, new_returned_date):
        self._returned_date = new_returned_date

    def __str__(self):
        rental_str = 'Rental: #' + str(self.rental_id) + '\nMovie: #' + str(self.movie_id)
        rental_str += '\nClient: #' + str(self.client_id) + '\nRented: ' + str(self.rented_date)
        rental_str += '\nDue: ' + str(self.due_date) + '\nReturned: ' + str(self.returned_date) + '\n'
        return rental_str

    def __len__(self):
        return (self.due_date - self.rented_date).days + 1
