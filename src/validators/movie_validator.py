from src.domain.movie import Movie
from src.validators.exceptions import MovieValidationException


class MovieValidator:

    @staticmethod
    def validate(movie: Movie):
        errors = []

        if movie.movie_id < 100:
            errors.append('Movie ID should have at least 3 digits!')
        if len(movie.title) < 3:
            errors.append('Movie title should have at least 3 letters!')
        if len(movie.description) < 5:
            errors.append('Movie description should have at least 5 letters!')
        if len(movie.genre) < 2:
            errors.append('Movie genre should have at least 2 letters!')

        if len(errors) > 0:
            raise MovieValidationException(errors)
