import unittest
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from unittest.mock import patch
from security.database import (
    create_user,
    authenticate_user,
    get_user_by_id,
    get_user_by_username,
    update_password,
)
from security.auth_utils import verify_password

Base = declarative_base()

# Minimal mock User model for testing
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TestDatabaseUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()

    @patch("security.database.logger")
    def test_create_user_and_get_user(self, mock_logger):
        user = create_user(self.db, "testuser", "user@validmail.com", "TestPass123!")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertTrue(verify_password("TestPass123!", user.password_hash))

        fetched_by_id = get_user_by_id(self.db, user.id)
        self.assertEqual(fetched_by_id.email, "user@validmail.com")

        fetched_by_username = get_user_by_username(self.db, "testuser")
        self.assertEqual(fetched_by_username.username, "testuser")

    @patch("security.database.logger")
    def test_authenticate_user_success(self, mock_logger):
        create_user(self.db, "authuser", "auth@validmail.com", "StrongPass456!")
        user = authenticate_user(self.db, "authuser", "StrongPass456!")
        self.assertIsNotNone(user)

        user_by_email = authenticate_user(self.db, "auth@validmail.com", "StrongPass456!")
        self.assertIsNotNone(user_by_email)
        self.assertEqual(user_by_email.username, "authuser")

    @patch("security.database.logger")
    def test_authenticate_user_failure(self, mock_logger):
        create_user(self.db, "failuser", "fail@validmail.com", "FailPass123!")
        wrong_pass = authenticate_user(self.db, "failuser", "WrongPass!")
        self.assertIsNone(wrong_pass)

        no_user = authenticate_user(self.db, "no_user", "AnyPass!")
        self.assertIsNone(no_user)

        empty_fields = authenticate_user(self.db, "", "")
        self.assertIsNone(empty_fields)

    @patch("security.database.logger")
    def test_update_password_success_and_failure(self, mock_logger):
        user = create_user(self.db, "updateuser", "update@validmail.com", "OldPass123!")
        self.assertIsNotNone(user)

        success = update_password(self.db, user.id, "NewStrongPass789!")
        self.assertTrue(success)

        authenticated = authenticate_user(self.db, "updateuser", "NewStrongPass789!")
        self.assertIsNotNone(authenticated)

        fail = update_password(self.db, 9999, "AnyPass!")
        self.assertFalse(fail)

        empty = update_password(self.db, user.id, "")
        self.assertFalse(empty)

    @patch("security.database.logger")
    def test_duplicate_user_creation(self, mock_logger):
        user1 = create_user(self.db, "dupeuser", "dupe@validmail.com", "Dup3Pass123!")
        self.assertIsNotNone(user1)

        user2 = create_user(self.db, "dupeuser", "unique@validmail.com", "Dup3Pass123!")
        self.assertIsNone(user2)  # No IntegrityError thrown; just returns None

        user3 = create_user(self.db, "uniqueuser", "dupe@validmail.com", "Dup3Pass123!")
        self.assertIsNone(user3)
    
    @patch("security.database.logger")
    def test_invalid_email_or_weak_password(self, mock_logger):
        user = create_user(self.db, "bademail", "invalidemail", "StrongPass1!")
        self.assertIsNone(user)

        user = create_user(self.db, "weakpass", "weak@validmail.com", "123")
        self.assertIsNone(user)
        

if __name__ == "__main__":
    unittest.main()
