import unittest
from simple_webserver.app import hello


class TestFlaskWebServer(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_hello(self):
        results = hello('Dan')
        self.assertEqual(results, 'Hello, Dan!')


if __name__ == '__main__':
    # run test with "python -m unittest simple_webserver/tests/test_flask_web.py"
    unittest.main()
