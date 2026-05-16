import unittest
from utils.validators import (
    validate_email,
    validate_url,
    validate_stock_symbol,
    validate_numeric_range,
    validate_date,
    validate_telegram_command,
    validate_telegram_user_id,
    validate_telegram_username,
    validate_password_strength,
    ValidationError,
)

class TestValidators(unittest.TestCase):

    def test_validate_email(self):
        self.assertTrue(validate_email("test.user@example.com"))
        self.assertTrue(validate_email("user+123@domain.co.uk"))
        with self.assertRaises(ValidationError):
            validate_email("invalid-email")
        with self.assertRaises(ValidationError):
            validate_email("noatsign.com")

    def test_validate_url(self):
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("https://sub.domain.com/path?query=1"))
        with self.assertRaises(ValidationError):
            validate_url("http://insecure.com")
        with self.assertRaises(ValidationError):
            validate_url("ftp://example.com")

    def test_validate_stock_symbol(self):
        self.assertTrue(validate_stock_symbol("AAPL"))
        self.assertTrue(validate_stock_symbol("TSLA"))
        self.assertTrue(validate_stock_symbol("BRK1"))
        with self.assertRaises(ValidationError):
            validate_stock_symbol("aapl")  # lowercase invalid
        with self.assertRaises(ValidationError):
            validate_stock_symbol("GOOG$")

    def test_validate_numeric_range(self):
        self.assertTrue(validate_numeric_range(5, 1, 10))
        self.assertTrue(validate_numeric_range(1, 1, 10))
        self.assertTrue(validate_numeric_range(10, 1, 10))
        with self.assertRaises(ValidationError):
            validate_numeric_range(0, 1, 10)
        with self.assertRaises(ValidationError):
            validate_numeric_range(11, 1, 10)
        with self.assertRaises(ValidationError):
            validate_numeric_range("not a number", 1, 10)

    def test_validate_date(self):
        self.assertTrue(validate_date("2025-05-30"))
        with self.assertRaises(ValidationError):
            validate_date("30-05-2025")
        with self.assertRaises(ValidationError):
            validate_date("2025/05/30")
        with self.assertRaises(ValidationError):
            validate_date(20250530)

    def test_validate_telegram_command(self):
        valid_cmds = ["/start", "/help", "/trade"]
        self.assertTrue(validate_telegram_command("/start", valid_cmds))
        self.assertTrue(validate_telegram_command("/trade", valid_cmds))
        with self.assertRaises(ValidationError):
            validate_telegram_command("start", valid_cmds)  # missing /
        with self.assertRaises(ValidationError):
            validate_telegram_command("/invalid!", valid_cmds)  # invalid char
        with self.assertRaises(ValidationError):
            validate_telegram_command("/notallowed", valid_cmds)  # not in whitelist

    def test_validate_telegram_user_id(self):
        self.assertTrue(validate_telegram_user_id(123456789))
        with self.assertRaises(ValidationError):
            validate_telegram_user_id(-1)
        with self.assertRaises(ValidationError):
            validate_telegram_user_id("notanint")

    def test_validate_telegram_username(self):
        self.assertTrue(validate_telegram_username("ValidUser_123"))
        self.assertTrue(validate_telegram_username("User123"))
        with self.assertRaises(ValidationError):
            validate_telegram_username("1InvalidStart")  # starts with digit
        with self.assertRaises(ValidationError):
            validate_telegram_username("_underscoreStart")
        with self.assertRaises(ValidationError):
            validate_telegram_username("shrt")  # too short
        with self.assertRaises(ValidationError):
            validate_telegram_username("a"*33)  # too long
        with self.assertRaises(ValidationError):
            validate_telegram_username("Invalid!Char")

    def test_validate_password_strength(self):
        self.assertTrue(validate_password_strength("StrongPass1!"))
        with self.assertRaises(ValidationError):
            validate_password_strength("weak")  # too short
        with self.assertRaises(ValidationError):
            validate_password_strength("alllowercase1!")
        with self.assertRaises(ValidationError):
            validate_password_strength("ALLUPPERCASE1!")
        with self.assertRaises(ValidationError):
            validate_password_strength("NoDigits!!")
        with self.assertRaises(ValidationError):
            validate_password_strength("NoSpecialChar1")

if __name__ == "__main__":
    unittest.main()
