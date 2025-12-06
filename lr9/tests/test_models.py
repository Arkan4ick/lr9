import unittest
from models.user import User
from models.currency import Currency

class TestModels(unittest.TestCase):
    def test_user_setters(self):
        u = User(1, 'Alice')
        self.assertEqual(u.id, 1)
        self.assertEqual(u.name, 'Alice')
        with self.assertRaises(TypeError):
            u.id = 'x'
        with self.assertRaises(ValueError):
            u.id = -5

    def test_currency_setters(self):
        c = Currency('R01235', 840, 'USD', 'US Dollar', 73.5, 1)
        self.assertEqual(c.char_code, 'USD')
        self.assertAlmostEqual(c.value, 73.5)
        with self.assertRaises(TypeError):
            c.nominal = 1.5
        with self.assertRaises(ValueError):
            c.nominal = 0

if __name__ == '__main__':
    unittest.main()
