"""
Бизнес-логика для сущности Currency.
Обёртка над CurrencyRatesCRUD для использования в маршрутах и тестах.
"""

from typing import List, Dict, Any, Optional
from controllers.databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    """Контроллер валют — использует CRUD-класс для операций."""

    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def list_currencies(self) -> List[Dict[str, Any]]:
        """Вернуть все валюты (list of dict)."""
        return self.db.list_all()

    def create_currency(self, currency_data: Dict[str, Any]) -> int:
        """Создать валюту и вернуть её id."""
        # можно добавить простую валидацию тут
        currency_data['char_code'] = currency_data['char_code'].upper()
        return self.db.add(currency_data)

    def update_currency_value(self, char_code: str, value: float) -> bool:
        """Обновить курс валюты. Возвращает True, если обновлено хотя бы 1 строка."""
        updated = self.db.update_value(char_code, value)
        return updated > 0

    def delete_currency(self, currency_id: int) -> bool:
        """Удалить валюту по id. Возвращает True, если удаление произошло."""
        deleted = self.db.delete(currency_id)
        return deleted > 0