import requests
import sys

def get_currencies(currency_codes: list, url:str = "https://www.cbr-xml-daily.ru/daily_json.js", handle=sys.stdout)->dict:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        currencies = {}
        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code].get("Value")
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies
    except requests.exceptions.RequestException as e:
        handle.write(f"Ошибка при запросе к API: {e}\n")
        raise
