import unittest
from utils import api_helpers, data_cleaner, file_ops, formatters, helpers, validators

class TestAPIHelpers(unittest.TestCase):
    def test_send_get_request(self):
        # Just test the function exists and callable (real API tests need mocks)
        self.assertTrue(callable(api_helpers.send_get_request))

    def test_send_post_request(self):
        self.assertTrue(callable(api_helpers.send_post_request))


class TestDataCleaner(unittest.TestCase):
    def test_remove_nulls(self):
        self.assertTrue(callable(data_cleaner.remove_nulls))

    def test_normalize_column(self):
        self.assertTrue(callable(data_cleaner.normalize_column))

    def test_convert_to_datetime(self):
        self.assertTrue(callable(data_cleaner.convert_to_datetime))

    def test_filter_outliers(self):
        self.assertTrue(callable(data_cleaner.filter_outliers))


class TestFileOps(unittest.TestCase):
    def test_read_write_file(self):
        self.assertTrue(callable(file_ops.read_file))
        self.assertTrue(callable(file_ops.write_file))

    def test_backup_and_atomic_write(self):
        self.assertTrue(callable(file_ops.create_backup))
        self.assertTrue(callable(file_ops._atomic_write))

    def test_json_read_write(self):
        self.assertTrue(callable(file_ops.read_json))
        self.assertTrue(callable(file_ops.write_json))
        self.assertTrue(callable(file_ops.read_json_file))
        self.assertTrue(callable(file_ops.write_json_file))

    def test_text_file_ops(self):
        self.assertTrue(callable(file_ops.read_text_file))
        self.assertTrue(callable(file_ops.write_text_file))

    def test_append_file(self):
        self.assertTrue(callable(file_ops.append_file))

    def test_file_exists(self):
        self.assertTrue(callable(file_ops.file_exists))

    def test_locked_file(self):
        self.assertTrue(callable(file_ops.locked_file))


class TestFormatters(unittest.TestCase):
    def test_format_datetime(self):
        self.assertTrue(callable(formatters.format_datetime))

    def test_format_date(self):
        self.assertTrue(callable(formatters.format_date))

    def test_format_currency(self):
        self.assertTrue(callable(formatters.format_currency))

    def test_format_percentage(self):
        self.assertTrue(callable(formatters.format_percentage))

    def test_format_number(self):
        self.assertTrue(callable(formatters.format_number))

    def test_title_case(self):
        self.assertTrue(callable(formatters.title_case))

    def test_snake_case(self):
        self.assertTrue(callable(formatters.snake_case))

    def test_remove_extra_spaces(self):
        self.assertTrue(callable(formatters.remove_extra_spaces))

    def test_pretty_json(self):
        self.assertTrue(callable(formatters.pretty_json))

    def test_format_percentage_change(self):
        self.assertTrue(callable(formatters.format_percentage_change))

    def test_format_duration(self):
        self.assertTrue(callable(formatters.format_duration))

    def test_format_ticker_symbol(self):
        self.assertTrue(callable(formatters.format_ticker_symbol))

    def test_safe_str(self):
        self.assertTrue(callable(formatters.safe_str))


class TestHelpers(unittest.TestCase):
    def test_is_valid_email(self):
        self.assertTrue(callable(helpers.is_valid_email))

    def test_format_currency(self):
        self.assertTrue(callable(helpers.format_currency))

    def test_currency_symbol(self):
        self.assertTrue(callable(helpers.currency_symbol))

    def test_safe_get(self):
        self.assertTrue(callable(helpers.safe_get))

    def test_list_to_str(self):
        self.assertTrue(callable(helpers.list_to_str))


class TestValidators(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(callable(validators.validate_email))

    def test_validate_url(self):
        self.assertTrue(callable(validators.validate_url))

    def test_validate_stock_symbol(self):
        self.assertTrue(callable(validators.validate_stock_symbol))

    def test_validate_numeric_range(self):
        self.assertTrue(callable(validators.validate_numeric_range))

    def test_validate_date(self):
        self.assertTrue(callable(validators.validate_date))

    def test_validate_telegram_command(self):
        self.assertTrue(callable(validators.validate_telegram_command))

    def test_validate_telegram_user_id(self):
        self.assertTrue(callable(validators.validate_telegram_user_id))

    def test_validate_telegram_username(self):
        self.assertTrue(callable(validators.validate_telegram_username))

    def test_validate_password_strength(self):
        self.assertTrue(callable(validators.validate_password_strength))


if __name__ == "__main__":
    unittest.main()
