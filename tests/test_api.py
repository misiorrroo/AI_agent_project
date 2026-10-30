import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

import requests

import api


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.api_key_patch = patch.object(api, "API_KEY", "test-api-key")
        self.api_key_patch.start()
        self.logger_patch = patch.object(api.logger, "error")
        self.logger_patch.start()

    def tearDown(self):
        self.logger_patch.stop()
        self.api_key_patch.stop()

    def make_response(self, body=None, status_code=200):
        response = Mock()
        response.status_code = status_code
        response.json.return_value = body
        response.raise_for_status.return_value = None
        return response

    def test_ask_ai_returns_response_content(self):
        response = self.make_response({
            "choices": [{"message": {"content": "Cześć!"}}],
        })

        with patch.object(api.requests, "post", return_value=response):
            self.assertEqual(api.ask_ai([], "test-model"), "Cześć!")

    def test_ask_ai_reports_http_error_and_returns_none(self):
        response = self.make_response(
            {"error": {"message": "Invalid API key"}},
            status_code=401,
        )
        response.raise_for_status.side_effect = requests.HTTPError(
            response=response,
        )

        with patch.object(api.requests, "post", return_value=response):
            output = io.StringIO()
            with redirect_stdout(output):
                result = api.ask_ai([], "test-model")

        self.assertIsNone(result)
        self.assertIn("Nieprawidłowy lub wygasły klucz API.", output.getvalue())
        self.assertIn("Invalid API key", output.getvalue())

    def test_ask_ai_reports_rate_limit(self):
        response = self.make_response(status_code=429)
        response.raise_for_status.side_effect = requests.HTTPError(
            response=response,
        )

        with patch.object(api.requests, "post", return_value=response):
            output = io.StringIO()
            with redirect_stdout(output):
                result = api.ask_ai([], "test-model")

        self.assertIsNone(result)
        self.assertIn("Przekroczono limit zapytań lub środków API.", output.getvalue())
        self.assertIn("HTTP 429", output.getvalue())

    def test_ask_ai_reports_timeout(self):
        with patch.object(api.requests, "post", side_effect=requests.Timeout):
            output = io.StringIO()
            with redirect_stdout(output):
                result = api.ask_ai([], "test-model")

        self.assertIsNone(result)
        self.assertIn("Przekroczono czas oczekiwania", output.getvalue())

    def test_ask_ai_reports_invalid_response(self):
        response = self.make_response()
        response.json.side_effect = ValueError("invalid JSON")

        with patch.object(api.requests, "post", return_value=response):
            output = io.StringIO()
            with redirect_stdout(output):
                result = api.ask_ai([], "test-model")

        self.assertIsNone(result)
        self.assertIn("Nieprawidłowa odpowiedź API.", output.getvalue())

    def test_ask_ai_reports_missing_api_key(self):
        with patch.object(api, "API_KEY", None):
            with patch.object(api.requests, "post") as post:
                output = io.StringIO()
                with redirect_stdout(output):
                    result = api.ask_ai([], "test-model")

        self.assertIsNone(result)
        self.assertIn("Brak klucza OPENROUTER_API_KEY", output.getvalue())
        post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
