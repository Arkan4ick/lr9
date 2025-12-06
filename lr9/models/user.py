class User:
    def __init__(self, user_id: int, name: str):
        self.id = user_id
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError('id must be int')
        if value < 0:
            raise ValueError('id must be non-negative')
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('name must be string')
        self._name = value
