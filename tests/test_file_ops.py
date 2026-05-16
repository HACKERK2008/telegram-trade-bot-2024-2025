import os
from pathlib import Path
import unittest
import tempfile
from utils import file_ops
from cryptography.fernet import Fernet

class TestFileOps(unittest.TestCase):

    def setUp(self):
        self.test_data = {"key": "value", "number": 42}
        self.test_text = "Hello, Secure World!"
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_file.json")
        self.backup_file = self.test_file + ".bak"
        self.secret_key = Fernet.generate_key()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_write_and_read_json_file(self):
        Path(self.test_file).write_text("{}", encoding="utf-8")  # Pre-create file to enable backup
        file_ops.write_json(self.test_file, self.test_data, backup=True)
        read_data = file_ops.read_json(self.test_file)
        self.assertEqual(read_data, self.test_data)
        self.assertTrue(os.path.exists(self.backup_file))

    def test_write_and_read_text_file(self):
        Path(self.test_file).write_text("", encoding="utf-8")  # Pre-create file to enable backup
        file_ops.write_file(self.test_file, self.test_text, backup=True)
        read_text = file_ops.read_file(self.test_file)
        self.assertEqual(read_text, self.test_text)
        self.assertTrue(os.path.exists(self.backup_file))


    def test_atomic_write_json(self):
        file_ops.write_json(self.test_file, self.test_data)
        with open(self.test_file, "r") as f:
            self.assertIn('"key": "value"', f.read())

    def test_write_json_with_encryption(self):
        file_ops.write_json(self.test_file, self.test_data, encrypt_key=self.secret_key)
        result = file_ops.read_json(self.test_file, decrypt_key=self.secret_key)
        self.assertEqual(result, self.test_data)

    def test_write_text_with_encryption(self):
        file_ops.write_file(self.test_file, self.test_text, encrypt_key=self.secret_key)
        result = file_ops.read_file(self.test_file, decrypt_key=self.secret_key)
        self.assertEqual(result, self.test_text)

    def test_invalid_json_file_returns_none(self):
        with open(self.test_file, "w") as f:
            f.write("not a json")
        result = file_ops.read_json(self.test_file)
        self.assertIsNone(result)

    def test_missing_file_returns_none(self):
        result = file_ops.read_file("nonexistent.txt")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
