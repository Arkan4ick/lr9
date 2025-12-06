class UserCurrency:
    def __init__(self, uc_id: int, user_id: int, currency_id: str):
        self.id = uc_id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError('id must be int')
        self._id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int):
            raise TypeError('user_id must be int')
        self._user_id = value

    @property
    def currency_id(self):
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value):
        if not isinstance(value, str):
            raise TypeError('currency_id must be str')
        self._currency_id = value
