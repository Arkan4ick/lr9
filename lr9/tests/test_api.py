import unittest
from unittest.mock import patch, Mock
from utils.currencies_api import get_currencies

class TestApi(unittest.TestCase):
    @patch('utilitiesutilities.currencies_api.requests.get')
    def test_get_currencies_success(self, mock_get):
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = {'Valute': {'USD': {'Value': 73.1}, 'EUR': {'Value': 86.2}}}
        mock_get.return_value = mock_resp
        data = get_currencies(['USD','EUR'])
        self.assertIn('USD', data)
        self.assertEqual(data['USD'], 73.1)

    @patch('utilitiesutilities.currencies_api.requests.get')
    def test_get_currencies_network_error(self, mock_get):
        mock_get.side_effect = Exception('network fail')
        with self.assertRaises(Exception):
            get_currencies(['USD'])

if __name__ == '__main__':
    unittest.main()
