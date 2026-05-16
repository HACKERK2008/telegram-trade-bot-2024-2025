import unittest
import time
from security import auth_utils


class TestAuthUtils(unittest.TestCase):

    def test_hash_and_verify_password(self):
        password = "My$ecureP@ss"
        hashed = auth_utils.hash_password(password)
        self.assertTrue(auth_utils.verify_password(password, hashed))
        self.assertFalse(auth_utils.verify_password("wrongpass", hashed))

    def test_generate_and_decode_jwt_token(self):
        data = {"user_id": 123, "role": "admin"}
        token = auth_utils.generate_jwt_token(data, expires_in=2)
        payload = auth_utils.decode_jwt_token(token)
        self.assertEqual(payload["user_id"], 123)
        self.assertEqual(payload["role"], "admin")

        time.sleep(3)  # Let token expire
        self.assertIsNone(auth_utils.decode_jwt_token(token))

    def test_generate_and_verify_otp(self):
        otp = auth_utils.generate_otp()
        expiry = time.time() + 2
        self.assertTrue(auth_utils.verify_otp(otp, otp, expiry))
        self.assertFalse(auth_utils.verify_otp("000000", otp, expiry))

        time.sleep(3)
        self.assertFalse(auth_utils.verify_otp(otp, otp, expiry))  # Expired now

    def test_is_authorized_telegram_user(self):
        allowed_users = {111, 222, 333}
        self.assertTrue(auth_utils.is_authorized_telegram_user(222, allowed_users))
        self.assertFalse(auth_utils.is_authorized_telegram_user(444, allowed_users))


if __name__ == "__main__":
    unittest.main()
