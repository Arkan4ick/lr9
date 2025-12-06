"""
Database controller: работа с SQLite (параметризованные запросы).
Реализует простые CRUD-операции для таблицы currency.
"""

from typing import List, Dict, Any, Optional
import sqlite3


class CurrencyRatesCRUD:
    """
    Контроллер для работы с таблицей currency.
    Экземпляр инициализируется sqlite3.Connection (можно ':memory:').
    """

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        # Для удобства включаем ограничение внешних ключей, если используются.
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.row_factory = sqlite3.Row

    def create_table(self) -> None:
        """Создать таблицу currency (если не существует)."""
        sql = """
        CREATE TABLE IF NOT EXISTS currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_code TEXT NOT NULL,
            char_code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            value REAL,
            nominal INTEGER
        )
        """
        self.conn.execute(sql)
        self.conn.commit()

    def add(self, data: Dict[str, Any]) -> int:
        """
        Добавить новую валюту.
        data: {"num_code": "...", "char_code": "...", "name": "...", "value": 0.0, "nominal": 1}
        Возвращает id новой записи.
        """
        sql = ("INSERT INTO currency (num_code, char_code, name, value, nominal) "
               "VALUES (:num_code, :char_code, :name, :value, :nominal)")
        cur = self.conn.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def list_all(self) -> List[Dict[str, Any]]:
        """Вернуть все валюты как список словарей."""
        cur = self.conn.execute("SELECT * FROM currency ORDER BY id")
        rows = cur.fetchall()
        return [dict(r) for r in rows]

    def get_by_char_code(self, char_code: str) -> Optional[Dict[str, Any]]:
        """Найти валюту по char_code."""
        cur = self.conn.execute("SELECT * FROM currency WHERE char_code = ?", (char_code.upper(),))
        row = cur.fetchone()
        return dict(row) if row else None

    def update_value(self, char_code: str, value: float) -> int:
        """
        Обновить курс валюты по char_code.
        Возвращает количество обновлённых строк.
        """
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        cur = self.conn.execute(sql, (value, char_code.upper()))
        self.conn.commit()
        return cur.rowcount

    def delete(self, currency_id: int) -> int:
        """Удалить валюту по id. Возвращает количество удалённых строк."""
        cur = self.conn.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.conn.commit()
        return cur.rowcount