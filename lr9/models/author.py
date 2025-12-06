class Author:
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('name must be a string')
        self._name = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if not isinstance(value, str):
            raise TypeError('group must be a string')
        self._group = value
