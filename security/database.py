from sqlalchemy.orm import Session
from database.models.user import User
from security.auth_utils import hash_password, verify_password, is_strong_password
from datetime import datetime, timezone
import logging
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create a new user with hashed password
def create_user(db: Session, username: str, email: str, password: str) -> User | None:
    if not username or not email or not password:
        logger.error("Username, email, and password are required.")
        raise ValueError("All fields must be non-empty.")

    # Email format validation
    try:
        valid_email = validate_email(email).normalized
    except EmailNotValidError as e:
        logger.error(f"Invalid email format: {email} - {str(e)}")
        return None

    # Password strength check
    if not is_strong_password(password):
        logger.error("Password does not meet strength requirements.")
        return None

    hashed_pw = hash_password(password)
    new_user = User(
        username=username,
        email=valid_email,
        password_hash=hashed_pw,
        created_at=datetime.now(timezone.utc)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"New user created: {username}")
        return new_user
    except IntegrityError as e:
        db.rollback()
        logger.error(f"User creation failed. Integrity error: {e.orig}")
        return None

# Authenticate user by username/email + password
def authenticate_user(db: Session, identifier: str, password: str) -> User | None:
    if not identifier or not password:
        logger.warning("Empty username/email or password during authentication.")
        return None

    user = db.query(User).filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if user and verify_password(password, user.password_hash):
        logger.info(f"User authenticated: {identifier}")
        return user

    logger.warning(f"Failed authentication attempt: {identifier}")
    return None

# Get user by ID
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

# Get user by username
def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

# Update user password securely
def update_password(db: Session, user_id: int, new_password: str) -> bool:
    if not new_password:
        logger.error("New password must not be empty.")
        return False

    if not is_strong_password(new_password):
        logger.error("New password does not meet strength requirements.")
        return False

    user = get_user_by_id(db, user_id)
    if user:
        user.password_hash = hash_password(new_password)
        db.commit()
        logger.info(f"Password updated for user_id: {user_id}")
        return True

    logger.error(f"Password update failed. User not found: {user_id}")
    return False
