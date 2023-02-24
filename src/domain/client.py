class Client:

    def __init__(self, client_id: int, name: str):
        self._client_id = client_id
        self._name = name

    @property
    def client_id(self):
        return self._client_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def __str__(self):
        client_str = '#' + str(self.client_id) + ': ' + self.name
        return client_str
