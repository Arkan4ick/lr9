"""
Главный файл приложения. Инициализирует БД в памяти, контроллеры и запускает HTTP-сервер.
Простой роутер: обрабатывает GET-запросы и выполняет CRUD + рендер.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sqlite3
import os

from controllers.databasecontroller import CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController
from controllers.pages import create_jinja_env, render_template

USERS = [
    {"id": 1, "name": "Семёнов Артём", "age": 18, "subscriptions": ["USD"]},
    {"id": 2, "name": "Торин Кирилл", "age": 17, "subscriptions": ["EUR", "USD"]},
    {"id": 3, "name": "Сергей Иванов", "age": 22, "subscriptions": []},
    {"id": 4, "name": "Туманов Михаил", "age": 18, "subscriptions": ["RUB"]},
    {"id": 5, "name": "Анна Соколова", "age": 33, "subscriptions": ["EUR"]},
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


def init_db() -> sqlite3.Connection:
    """Инициализация подключения в памяти и заполнение тестовыми данными."""
    conn = sqlite3.connect(":memory:")
    db = CurrencyRatesCRUD(conn)
    db.create_table()
    # Простейшие стартовые данные
    data = [
        {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
        {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 100.0, "nominal": 1},
        {"num_code": "643", "char_code": "RUB", "name": "Российский рубль", "value": 1.0, "nominal": 1},
    ]
    for d in data:
        try:
            db.add(d)
        except Exception:
            pass
    return conn


class RequestHandler(BaseHTTPRequestHandler):
    """Простой HTTP GET-роутер."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Получаем доступ к окружению Jinja2 и контроллерам через серверный объект
        env = self.server.jinja_env
        currency_ctrl: CurrencyController = self.server.currency_controller

        # Главная
        if path == "/":
            currencies = currency_ctrl.list_currencies()
            body = render_template(env, "index.html", {"currencies": currencies})
            self._send_html(body)
            return

        # Список валют
        if path == "/currencies":
            currencies = currency_ctrl.list_currencies()
            body = render_template(env, "currencies.html", {"currencies": currencies})
            self._send_html(body)
            return

        # Удалить валюту по id: /currency/delete?id=1
        if path == "/currency/delete":
            try:
                cid = int(qs.get("id", [""])[0])
                currency_ctrl.delete_currency(cid)
            except Exception:
                pass
            # Редирект на список валют (простая реализация — вернуть страницу)
            currencies = currency_ctrl.list_currencies()
            body = render_template(env, "currencies.html", {"currencies": currencies})
            self._send_html(body)
            return

        # Обновление курса через query: /currency/update?USD=95.5
        if path == "/currency/update":
            # берем первый парамет: USD=95.5
            if qs:
                for key, val in qs.items():
                    try:
                        new_value = float(val[0])
                        char_code = key.upper()
                        currency_ctrl.update_currency_value(char_code, new_value)
                    except Exception:
                        continue
            currencies = currency_ctrl.list_currencies()
            body = render_template(env, "currencies.html", {"currencies": currencies})
            self._send_html(body)
            return

        # Страница "об авторе"
        if path == "/author":
            body = render_template(env, "author.html", {"title": "Об авторе"})
            self._send_html(body)
            return

        # Список пользователей (тестовые данные)
        if path == "/users":
            body = render_template(env, "users.html", {
                "users": USERS
            })
            self._send_html(body)
            return

        # Страница одного пользователя: /user?id=3
        if path == "/user":
            try:
                user_id = int(qs.get("id", [""])[0])
                user = next((u for u in USERS if u["id"] == user_id), None)
            except Exception:
                user = None

            body = render_template(env, "user.html", {
                "user": user,
                "currencies": currency_ctrl.list_currencies()
            })
            self._send_html(body)
            return

        # Подписаться на валюту
        if path == "/subscribe":
            try:
                user_id = int(qs.get("user_id", [""])[0])
                currency = qs.get("currency", [""])[0].upper()

                user = next((u for u in USERS if u["id"] == user_id), None)
                if user and currency not in user["subscriptions"]:
                    user["subscriptions"].append(currency)

            except Exception as e:
                print("ERROR subscribe:", e)

            body = render_template(env, "user.html", {
                "user": user,
                "currencies": currency_ctrl.list_currencies()
            })
            self._send_html(body)
            return

        # Удалить валюту из подписок
        if path == "/unsubscribe":
            try:
                user_id = int(qs.get("user_id", [""])[0])
                currency = qs.get("currency", [""])[0].upper()

                user = next((u for u in USERS if u["id"] == user_id), None)
                if user and currency in user["subscriptions"]:
                    user["subscriptions"].remove(currency)

            except Exception as e:
                print("ERROR unsubscribe:", e)

            body = render_template(env, "user.html", {
                "user": user,
                "currencies": currency_ctrl.list_currencies()
            })
            self._send_html(body)
            return

        # Добавление валюты (форма)
        if path == "/currency/add_form":
            body = render_template(env, "add_currency.html", {})
            self._send_html(body)
            return

        # Добавление валюты
        if path == "/currency/add":
            try:
                num_code = qs.get("num_code", [""])[0]
                char_code = qs.get("char_code", [""])[0]
                name = qs.get("name", [""])[0]
                value = float(qs.get("value", ["0"])[0])
                nominal = int(qs.get("nominal", ["1"])[0])

                currency_ctrl.create_currency({
                    "num_code": num_code,
                    "char_code": char_code,
                    "name": name,
                    "value": value,
                    "nominal": nominal
                })

            except Exception as e:
                print("ERROR add currency:", e)

            currencies = currency_ctrl.list_currencies()
            body = render_template(env, "currencies.html", {"currencies": currencies})
            self._send_html(body)
            return

        # Прочие маршруты — 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not found")

    def _send_html(self, body: str, status: int = 200):
        body_bytes = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)


def run(port: int = 8000):
    conn = init_db()
    db = CurrencyRatesCRUD(conn)
    currency_controller = CurrencyController(db)
    jinja_env = create_jinja_env(TEMPLATE_DIR)

    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, RequestHandler)
    # подшиваем контроллеры и env к серверному объекту, чтобы handler их видел
    httpd.jinja_env = jinja_env
    httpd.currency_controller = currency_controller

    print(f"Starting server on http://127.0.0.1:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server")
        httpd.server_close()


run(8000)