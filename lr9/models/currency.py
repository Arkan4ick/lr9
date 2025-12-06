from typing import Optional


class Currency:

    def __init__(self,
                 currency_id: Optional[int],
                 num_code: str,
                 char_code: str,
                 name: str,
                 value: float = 0.0,
                 nominal: int = 1):
        self.id = currency_id
        self.num_code = num_code
        self.char_code = char_code.upper()
        self.name = name
        self.value = float(value)
        self.nominal = int(nominal)

    @property
    def char_code(self) -> str:
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str) -> None:
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.__char_code = val.upper()

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, val: float) -> None:
        if float(val) < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self.__value = float(val)

    def to_dict(self) -> dict:
        """Преобразовать в словарь для хранения/рендера."""
        return {
            "id": self.id,
            "num_code": self.num_code,
            "char_code": self.__char_code,
            "name": self.name,
            "value": self.__value,
            "nominal": self.nominal
        }