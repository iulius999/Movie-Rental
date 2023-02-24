from datetime import date
from src.services.client_service import ClientService
from src.services.movie_service import MovieService
from src.services.rental_service import RentalService
from src.services.undo_service import UndoService
from src.validators.exceptions import MovieValidationException, ServiceException, RepositoryException, \
    ClientValidationException, RentalValidationException, UndoException


class UI:

    def __init__(self, movie_service: MovieService, client_service: ClientService, rental_service: RentalService,
                 undo_service: UndoService):
        self._movie_service = movie_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._undo_service = undo_service
        print('\nWelcome! In order to choose an option, type its corresponding number.')
        self._options = {
            '1': self._manage_movies,
            '2': self._manage_clients,
            '3': self._manage_rentals,
            '4': self._statistics,
            '5': self._undo,
            '0': self._exit
        }

    def start(self):
        while True:
            self._display_options()
            opt = input('>>> ')
            opt = opt.strip()

            try:
                self._options[opt]()
            except KeyError:
                print('Invalid option!')

    @staticmethod
    def _display_options():
        print()
        print('Menu:')
        print('\t1. Manage movies')
        print('\t2. Manage clients')
        print('\t3. Manage rentals')
        print('\t4. Statistics')
        print('\t5. Undo')
        print('\t0. Exit')

    def _manage_movies(self):
        options = {
            '1': self._add_movie,
            '2': self._remove_movie,
            '3': self._update_movie,
            '4': self._display_all_movies,
            '5': self._search_movies
        }

        print()
        print('Menu:')
        print('\t1. Add a movie')
        print('\t2. Remove a movie')
        print('\t3. Update a movie')
        print('\t4. Display all movies')
        print('\t5. Search movies')

        opt = input('>>> ')
        opt = opt.strip()

        try:
            options[opt]()
        except KeyError:
            print('Invalid option!')

    def _add_movie(self):
        movie_id = input('Movie ID: ')
        title = input('Title: ')
        description = input('Description: ')
        genre = input('Genre: ')

        try:
            movie_id = int(movie_id)
            self._movie_service.add(movie_id, title, description, genre)
            print('Movie added successfully!')
        except ValueError:
            print('Movie ID should be a positive integer having at least 3 digits!')
        except MovieValidationException as mve:
            print(str(mve))
        except RepositoryException as re:
            print(str(re))

    def _remove_movie(self):
        movie_id = input('Movie ID: ')

        try:
            movie_id = int(movie_id)
            self._movie_service.remove(movie_id)
            print('Movie removed successfully!')
        except ValueError:
            print('Movie ID should be a positive integer having at least 3 digits!')
        except ServiceException as se:
            print(str(se))
        except RepositoryException as re:
            print(str(re))

    def _update_movie(self):
        options = {
            '1': self._update_movie_title,
            '2': self._update_movie_description,
            '3': self._update_movie_genre
        }

        print()
        print('Menu:')
        print('\t1. Update movie title')
        print('\t2. Update movie description')
        print('\t3. Update movie genre')

        opt = input('>>> ')
        opt = opt.strip()

        try:
            options[opt]()
        except KeyError:
            print('Invalid command!')

    def _update_movie_title(self):
        movie_id = input('Movie ID: ')
        new_title = input('New title: ')

        try:
            movie_id = int(movie_id)
            self._movie_service.update_title(movie_id, new_title)
            print('Movie title updated successfully!')
        except ValueError:
            print('Movie ID should be a positive integer having at least 3 digits!')
        except ServiceException as se:
            print(str(se))
        except RepositoryException as re:
            print(str(re))

    def _update_movie_description(self):
        movie_id = input('Movie ID: ')
        new_description = input('New description: ')

        try:
            movie_id = int(movie_id)
            self._movie_service.update_description(movie_id, new_description)
            print('Movie description updated successfully!')
        except ValueError:
            print('Movie ID should be a positive integer having at least 3 digits!')
        except ServiceException as se:
            print(str(se))
        except RepositoryException as re:
            print(str(re))

    def _update_movie_genre(self):
        movie_id = input('Movie ID: ')
        new_genre = input('New genre: ')

        try:
            movie_id = int(movie_id)
            self._movie_service.update_genre(movie_id, new_genre)
            print('Movie genre updated successfully!')
        except ValueError:
            print('Movie ID should be a positive integer having at least 3 digits!')
        except ServiceException as se:
            print(str(se))
        except RepositoryException as re:
            print(str(re))

    def _display_all_movies(self):
        if self._movie_service.size() == 0:
            print('Movie repository is empty!')
            return

        for movie in self._movie_service.get_all():
            print(movie)

    def _search_movies(self):
        something = input('Search for: ')
        something = something.strip()

        movies = self._movie_service.search(something)
        if len(movies) == 0:
            print('No movies found!')
            return

        for movie in movies:
            print(movie)

    def _manage_clients(self):
        options = {
            '1': self._add_client,
            '2': self._remove_client,
            '3': self._update_client_name,
            '4': self._display_all_clients,
            '5': self._search_clients
        }

        print()
        print('Menu:')
        print('\t1. Add a client')
        print('\t2. Remove a client')
        print('\t3. Update a client')
        print('\t4. Display all clients')
        print('\t5. Search clients')

        opt = input('>>> ')
        opt = opt.strip()

        try:
            options[opt]()
        except KeyError:
            print('Invalid option!')

    def _add_client(self):
        client_id = input('Client ID: ')
        name = input('Name: ')

        try:
            client_id = int(client_id)
            self._client_service.add(client_id, name)
            print('Client added successfully!')
        except ValueError:
            print('Client ID should be a positive integer having at least 3 digits!')
        except ClientValidationException as cve:
            print(str(cve))
        except RepositoryException as re:
            print(str(re))

    def _remove_client(self):
        client_id = input('Client ID: ')

        try:
            client_id = int(client_id)
            self._rental_service.remove_client(client_id)
            self._client_service.remove(client_id)
            print('Client removed successfully!')
        except ValueError:
            print('Client ID should be a positive integer having at least 3 digits!')
        except ServiceException as se:
            print(str(se))
        except RepositoryException as re:
            print(str(re))

    def _update_client_name(self):
        client_id = input('Client ID: ')
        new_name = input('New name: ')

        try:
            client_id = int(client_id)
            self._client_service.update_name(client_id, new_name)
            print('Client name updated successfully!')
        except ValueError:
            print('Client ID should be a positive integer having at least 3 digits!')
        except ServiceException as se:
            print(str(se))
        except RepositoryException as re:
            print(str(re))

    def _display_all_clients(self):
        if self._client_service.size() == 0:
            print('Client repository is empty!')
            return

        for client in self._client_service.get_all():
            print(client)

    def _search_clients(self):
        something = input('Search for: ')
        something = something.strip()

        clients = self._client_service.search(something)
        if len(clients) == 0:
            print('No clients found!')
            return

        for client in clients:
            print(client)

    def _manage_rentals(self):
        options = {
            '1': self._rent_movie,
            '2': self._return_movie,
            '3': self._display_all_rentals
        }

        print()
        print('Menu:')
        print('\t1. Rent a movie')
        print('\t2. Return a movie')
        print('\t3. Display all rentals')

        opt = input('>>> ')
        opt = opt.strip()

        try:
            options[opt]()
        except KeyError:
            print('Invalid option!')

    def _rent_movie(self):
        rental_id = input('Rental ID: ')
        movie_id = input('Movie ID: ')
        client_id = input('Client ID: ')
        print()

        rent_year = input('Rent date year: ')
        rent_month = input('Rent date month: ')
        rent_day = input('Rent date day: ')
        print()

        due_year = input('Due date year: ')
        due_month = input('Due date month: ')
        due_day = input('Due date day: ')
        print()

        try:
            rental_id = int(rental_id)
            movie_id = int(movie_id)
            client_id = int(client_id)

            rent_year = int(rent_year)
            rent_month = int(rent_month)
            rent_day = int(rent_day)

            due_year = int(due_year)
            due_month = int(due_month)
            due_day = int(due_day)

            rent_date = date(rent_year, rent_month, rent_day)
            due_date = date(due_year, due_month, due_day)

            self._rental_service.add(rental_id, movie_id, client_id, rent_date, due_date, None)
            print('Movie rented successfully!')

        except ValueError as ve:
            if str(ve).startswith('invalid'):
                print('Invalid format. Positive integers expected!')
            else:
                print('Invalid date!')

        except RentalValidationException as rve:
            print(str(rve))

        except RepositoryException as re:
            print(str(re))

        except ServiceException as se:
            print(str(se))

    def _return_movie(self):
        rental_id = input('Rental ID: ')

        return_year = input('Return date year: ')
        return_month = input('Return date month: ')
        return_day = input('Return date day: ')

        try:
            rental_id = int(rental_id)

            return_year = int(return_year)
            return_month = int(return_month)
            return_day = int(return_day)

            return_date = date(return_year, return_month, return_day)

            self._rental_service.update_returned_date(rental_id, return_date)
            print('Movie returned successfully!')

        except ValueError as ve:
            if str(ve).startswith('invalid'):
                print('Invalid format. Positive integers expected!')
            else:
                print('Invalid date!')

        except RepositoryException as re:
            print(str(re))

        except ServiceException as se:
            print(str(se))

    def _display_all_rentals(self):
        if self._rental_service.size() == 0:
            print('Rental repository is empty!')

        for rental in self._rental_service.get_all():
            print(rental)

    def _statistics(self):
        options = {
            '1': self._most_rented_movies,
            '2': self._most_active_clients,
            '3': self._late_rentals
        }

        print()
        print('Menu:')
        print('\t1. Most rented movies')
        print('\t2. Most active clients')
        print('\t3. Late rentals')

        opt = input('>>> ')
        opt = opt.strip()

        try:
            options[opt]()
        except KeyError:
            print('Invalid option!')

    def _most_rented_movies(self):
        results = self._rental_service.most_rented_movies()
        if len(results) == 0:
            print('No movies were rented!')
            return

        for dto in results:
            print(dto)

    def _most_active_clients(self):
        results = self._rental_service.most_active_clients()
        if len(results) == 0:
            print('Nobody rented a movie!')
            return

        for dto in results:
            print(dto)

    def _late_rentals(self):
        print('Late rentals for...')
        year = input('Year: ')
        month = input('Month: ')
        day = input('Day: ')
        print()

        try:
            year = int(year)
            month = int(month)
            day = int(day)
            today = date(year, month, day)
        except ValueError:
            print('Invalid date!')
            return

        results = self._rental_service.late_rentals(today)
        if len(results) == 0:
            print('No late rentals!')
            return

        for dto in results:
            print(dto)

    def _undo(self):
        try:
            self._undo_service.undo()
            print('Operation undone successfully!')
        except UndoException as ue:
            print(str(ue))

    @staticmethod
    def _exit():
        print('Exiting the application...')
        exit(0)
