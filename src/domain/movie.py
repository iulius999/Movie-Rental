class Movie:

    def __init__(self, movie_id: int, title: str, description: str, genre: str):
        self._movie_id = movie_id
        self._title = title
        self._description = description
        self._genre = genre

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, new_genre):
        self._genre = new_genre

    def __str__(self):
        movie_str = '#' + str(self.movie_id) + ': ' + self.title + '\n'
        movie_str += self.description + '\n' + 'Genre: ' + self.genre + '\n'
        return movie_str
