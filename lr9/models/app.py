from .author import Author
class App:
    def __init__(self, name: str, version: str, author: Author):
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('name must be a string')
        self._name = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if not isinstance(value, str):
            raise TypeError('version must be a string')
        self._version = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError('author must be an Author instance')
        self._author = value
