import unittest
from utils import formatters
import datetime

class TestFormatters(unittest.TestCase):

    def test_format_datetime(self):
        dt = datetime.datetime(2023, 1, 2, 15, 30, 45)
        self.assertEqual(formatters.format_datetime(dt), "2023-01-02 15:30:45")
        self.assertEqual(formatters.format_datetime("2023-01-02T15:30:45"), "2023-01-02 15:30:45")
        self.assertEqual(formatters.format_datetime(None), "")
        self.assertEqual(formatters.format_datetime("invalid"), "invalid")
    
    def test_format_date(self):
        d = datetime.date(2023, 1, 2)
        self.assertEqual(formatters.format_date(d), "2023-01-02")
        self.assertEqual(formatters.format_date("2023-01-02"), "2023-01-02")
        self.assertEqual(formatters.format_date(None), "")
        self.assertEqual(formatters.format_date("invalid"), "invalid")

    def test_format_currency(self):
        self.assertEqual(formatters.format_currency(1234.567), "$1,234.57")
        self.assertEqual(formatters.format_currency(None), "")
        self.assertEqual(formatters.format_currency(1234.5, symbol="€", decimals=1), "€1,234.5")
        self.assertEqual(formatters.format_currency("abc"), "")

    def test_format_percentage(self):
        self.assertEqual(formatters.format_percentage(0.1234), "12.34%")
        self.assertEqual(formatters.format_percentage(None), "")
        self.assertEqual(formatters.format_percentage(1, decimals=0), "100%")
        self.assertEqual(formatters.format_percentage("abc"), "")

    def test_format_number(self):
        self.assertEqual(formatters.format_number(12345.6789), "12,345.68")
        self.assertEqual(formatters.format_number(None), "")
        self.assertEqual(formatters.format_number(12345.6, decimals=1), "12,345.6")
        self.assertEqual(formatters.format_number("abc"), "")

    def test_title_case(self):
        self.assertEqual(formatters.title_case("hello world"), "Hello World")
        self.assertEqual(formatters.title_case(None), "")
        self.assertEqual(formatters.title_case(""), "")
    
    def test_snake_case(self):
        self.assertEqual(formatters.snake_case("Hello World-Test!"), "hello_world_test")
        self.assertEqual(formatters.snake_case(None), "")
        self.assertEqual(formatters.snake_case(""), "")
    
    def test_remove_extra_spaces(self):
        self.assertEqual(formatters.remove_extra_spaces("  Hello   World  "), "Hello World")
        self.assertEqual(formatters.remove_extra_spaces(None), "")
        self.assertEqual(formatters.remove_extra_spaces(""), "")

    def test_pretty_json(self):
        data = {"b": 1, "a": 2}
        result = formatters.pretty_json(data)
        self.assertTrue(result.startswith("{"))
        self.assertIn('"a": 2', result)
        self.assertEqual(formatters.pretty_json(None), "")
        self.assertEqual(formatters.pretty_json("invalid"), "")

    def test_format_percentage_change(self):
        self.assertEqual(formatters.format_percentage_change(120, 100), "+20.00%")
        self.assertEqual(formatters.format_percentage_change(80, 100), "-20.00%")
        self.assertEqual(formatters.format_percentage_change(None, 100), "")
        self.assertEqual(formatters.format_percentage_change(100, 0), "")
        self.assertEqual(formatters.format_percentage_change(100, None), "")

    def test_format_duration(self):
        self.assertEqual(formatters.format_duration(3661), "1:01:01")
        self.assertEqual(formatters.format_duration("3600"), "1:00:00")
        self.assertEqual(formatters.format_duration(None), "")
        self.assertEqual(formatters.format_duration("invalid"), "")

    def test_format_ticker_symbol(self):
        self.assertEqual(formatters.format_ticker_symbol(" aapl "), "AAPL")
        self.assertEqual(formatters.format_ticker_symbol(None), "")
        self.assertEqual(formatters.format_ticker_symbol(""), "")

    def test_safe_str(self):
        self.assertEqual(formatters.safe_str(123), "123")
        self.assertEqual(formatters.safe_str(None), "")
        self.assertEqual(formatters.safe_str("abc"), "abc")


if __name__ == "__main__":
    unittest.main()
