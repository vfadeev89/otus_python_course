import hashlib
import unittest
import api
from functools import wraps
from datetime import datetime


def cases(cases_list):
    def decorator(func):
        @wraps(func)
        def wrapper(*func_args):
            for case in cases_list:
                func(*func_args + (case,))
        return wrapper
    return decorator


class StoreMock:
    def __init__(self, is_available=True):
        self.is_available = is_available
        self.store = {}

    def get(self, key):
        if self.is_available:
            return self.store.get(key, None)
        raise RuntimeError

    def cache_get(self, key):
        if self.is_available:
            return self.store.get(key, None)
        return None

    def cache_set(self, key, value, expires=0):
        if self.is_available:
            self.store[key] = value


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store = StoreMock()

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    def set_valid_token(self, request):
        if request["login"] == api.ADMIN_LOGIN:
            request["token"] = hashlib.sha512(datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT).hexdigest()
        else:
            request["token"] = hashlib.sha512(request["account"] + request["login"] + api.SALT).hexdigest()

    def test_empty_request(self):
        _, code = self.get_response({})
        self.assertEqual(api.INVALID_REQUEST, code)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "sdd", "arguments": {}},
        {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": "", "arguments": {}},
    ])
    def test_bad_auth(self, request):
        response, code = self.get_response(request)
        self.assertEqual(code, api.FORBIDDEN)

    @cases([
        {"account": "", "login": "h&f", "arguments": {}},
        {"account": "", "login": "h&f", "method": "online_score"},
        {"account": "", "login": "admin", "method": "online_score", "arguments": {}},
    ])
    def test_invalid_request(self, request):
        self.set_valid_token(request)
        response, code = self.get_response(request)
        self.assertEqual(code, api.INVALID_REQUEST)

    @cases([
        {},
        {"phone": "79175302441"},
        {"phone": "89175302441", "email": "bad@ass.us"},
        {"phone": "79175302441", "email": "badass.us"},
        {"phone": "79175302441", "email": "bad@ass.us", "gender": -1},
        {"phone": "79175302441", "email": "bad@ass.us", "gender": "1"},
        {"phone": "79175302441", "email": "bad@ass.us", "gender": 1, "birthday": "01.01.1600"},
        {"phone": "79175302441", "email": "bad@ass.us", "gender": 1, "birthday": "XXX"},
        {"phone": "79175302441", "email": "bad@ass.us", "gender": 1, "birthday": "01.01.2005", "first_name": 1},
        {"phone": "79175302441", "email": "bad@ass.us", "gender": 1, "birthday": "01.01.2010","first_name": "b",
         "last_name": 2},
        {"phone": "79175302441", "birthday": "01.01.2000", "first_name": "s"},
        {"email": "bad@ass.us", "gender": 1, "last_name": 2},
    ])
    def test_invalid_score_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_token(request)
        response, code = self.get_response(request)
        self.assertEqual(code, api.INVALID_REQUEST)

    @cases([
        {"phone": "79175302441", "email": "bad@ass.us"},
        {"phone": 79175302441, "email": "bad@ass.us"},
        {"gender": 1, "birthday": "01.01.2000", "first_name": "a", "last_name": "b"},
        {"gender": 0, "birthday": "01.01.2000"},
        {"gender": 2, "birthday": "01.01.2000"},
        {"first_name": "a", "last_name": "b"},
        {"phone": "79175302441", "email": "bad@ass.us", "gender": 1, "birthday": "01.01.2000",
         "first_name": "a", "last_name": "b"},
    ])
    def test_ok_score_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_token(request)
        response, code = self.get_response(request)
        self.assertEqual(api.OK, code, arguments)
        score = response.get("score")
        self.assertTrue(isinstance(score, (int, float)) and score >= 0, arguments)
        self.assertEqual(sorted(self.context["has"]), sorted(arguments.keys()))

    def test_ok_score_admin_request(self):
        arguments = {"phone": "79175302441", "email": "bad@ass.us"}
        request = {"account": "horns&hoofs", "login": "admin", "method": "online_score", "arguments": arguments}
        self.set_valid_token(request)
        response, code = self.get_response(request)
        self.assertEqual(api.OK, code)
        score = response.get("score")
        self.assertEqual(score, 42)

    @cases([
        {},
        {"date": "07.04.2018"},
        {"client_ids": ["1", "2"], "date": "07.04.2018"},
        {"client_ids": [], "date": "07.04.2018"},
        {"client_ids": [1, 2], "date": "XXX"},
        {"client_ids": {1: 2}, "date": "07.04.2018"},
    ])
    def test_invalid_interests_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        self.set_valid_token(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"client_ids": [1, 2, 3], "date": datetime.today().strftime("%d.%m.%Y")},
        {"client_ids": [0]},
        {"client_ids": [1, 2], "date": "07.04.2018"},
    ])
    def test_ok_interests_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        self.set_valid_token(request)
        response, code = self.get_response(request)
        self.assertEqual(api.OK, code, arguments)
        self.assertEqual(len(arguments["client_ids"]), len(response))
        self.assertEqual(len(arguments["client_ids"]), len(response))
        self.assertTrue(all(v and isinstance(v, list) and all(isinstance(i, basestring) for i in v)
                            for v in response.values()))
        self.assertEqual(self.context.get("nclients"), len(arguments["client_ids"]))


if __name__ == "__main__":
    unittest.main()
