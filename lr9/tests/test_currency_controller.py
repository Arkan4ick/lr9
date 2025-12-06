import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController


class TestCurrencyController(unittest.TestCase):
    def test_list_currencies_calls_db(self):
        mock_db = MagicMock()
        mock_db.list_all.return_value = [{"id": 1, "char_code": "USD", "value": 90.0}]
        ctrl = CurrencyController(mock_db)
        result = ctrl.list_currencies()
        self.assertEqual(len(result), 1)
        mock_db.list_all.assert_called_once()

    def test_update_currency_value_returns_true_on_success(self):
        mock_db = MagicMock()
        mock_db.update_value.return_value = 1  # одна строка обновлена
        ctrl = CurrencyController(mock_db)
        ok = ctrl.update_currency_value("usd", 95.0)
        self.assertTrue(ok)
        mock_db.update_value.assert_called_once_with("usd", 95.0)