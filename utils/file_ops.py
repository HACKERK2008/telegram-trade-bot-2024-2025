# utils/file_ops.py

import os
import json
import tempfile
import shutil
import logging
from typing import Optional, Union
from threading import Lock
from contextlib import contextmanager
from cryptography.fernet import Fernet, InvalidToken

# Thread lock for file operations
_file_lock = Lock()

# Setup logger for audit and error tracing
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to INFO or WARNING in production
handler = logging.FileHandler('file_ops.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@contextmanager
def locked_file():
    """
    Context manager for thread-safe file operations.
    """
    _file_lock.acquire()
    try:
        yield
    finally:
        _file_lock.release()


def _atomic_write(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    Write content atomically to avoid partial writes.
    """
    try:
        dir_name = os.path.dirname(file_path)
        with tempfile.NamedTemporaryFile('w', delete=False, encoding=encoding, dir=dir_name) as tmp_file:
            tmp_file.write(content)
            temp_name = tmp_file.name
        shutil.move(temp_name, file_path)
        return True
    except Exception as e:
        logger.error(f"Atomic write failed for {file_path}: {e}")
        return False


def create_backup(file_path: str) -> bool:
    """
    Create a backup copy of the file with .bak extension.
    """
    backup_path = f"{file_path}.bak"
    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"Backup created for {file_path} at {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Backup failed for {file_path}: {e}")
        return False


def read_file(file_path: str, encoding: str = 'utf-8', decrypt_key: Optional[bytes] = None) -> Optional[str]:
    """
    Read text file content, optionally decrypt.

    Args:
        file_path: File path
        encoding: File encoding
        decrypt_key: Optional bytes key for decrypting the content

    Returns:
        File content or None if error.
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            data = f.read()

        if decrypt_key:
            fernet = Fernet(decrypt_key)
            try:
                data = fernet.decrypt(data.encode()).decode(encoding)
            except InvalidToken:
                logger.error("Decryption failed: Invalid key or corrupted data")
                return None

        return data
    except Exception as e:
        logger.error(f"Read failed for {file_path}: {e}")
        return None


def write_file(
    file_path: str,
    content: str,
    encoding: str = 'utf-8',
    backup: bool = True,
    encrypt_key: Optional[bytes] = None,
    set_permissions: Optional[int] = None  # e.g. 0o600
) -> bool:
    """
    Write text file atomically with optional backup, encryption, and permission setting.

    Args:
        file_path: File path
        content: Text to write
        encoding: File encoding
        backup: Create backup before overwrite
        encrypt_key: Optional bytes key for encrypting content
        set_permissions: Optional octal permissions to set

    Returns:
        Success boolean
    """
    with locked_file():
        try:
            if backup and os.path.exists(file_path):
                create_backup(file_path)

            if encrypt_key:
                fernet = Fernet(encrypt_key)
                content = fernet.encrypt(content.encode(encoding)).decode(encoding)

            success = _atomic_write(file_path, content, encoding)

            if success and set_permissions is not None:
                os.chmod(file_path, set_permissions)

            return success
        except Exception as e:
            logger.error(f"Write failed for {file_path}: {e}")
            return False


def append_file(
    file_path: str,
    content: str,
    encoding: str = 'utf-8',
    encrypt_key: Optional[bytes] = None,
    set_permissions: Optional[int] = None
) -> bool:
    """
    Append to file with optional encryption and permission setting.
    Note: appending encrypted content as-is (not encrypting whole file)

    Args:
        file_path: File path
        content: Text to append
        encoding: File encoding
        encrypt_key: Optional bytes key for encrypting appended content
        set_permissions: Optional octal permissions to set

    Returns:
        Success boolean
    """
    with locked_file():
        try:
            if encrypt_key:
                fernet = Fernet(encrypt_key)
                content = fernet.encrypt(content.encode(encoding)).decode(encoding)

            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)

            if set_permissions is not None:
                os.chmod(file_path, set_permissions)

            return True
        except Exception as e:
            logger.error(f"Append failed for {file_path}: {e}")
            return False


def file_exists(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: File path

    Returns:
        True if exists else False
    """
    exists = os.path.isfile(file_path)
    logger.debug(f"File exists check for {file_path}: {exists}")
    return exists


def read_json(
    file_path: str,
    encoding: str = 'utf-8',
    decrypt_key: Optional[bytes] = None
) -> Optional[Union[dict, list]]:
    """
    Read JSON file, optionally decrypt.

    Args:
        file_path: JSON file path
        encoding: File encoding
        decrypt_key: Optional bytes key for decrypting content

    Returns:
        Parsed JSON or None on failure
    """
    content = read_file(file_path, encoding, decrypt_key)
    if content is None:
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {file_path}: {e}")
        return None


def write_json(
    file_path: str,
    data: Union[dict, list],
    encoding: str = 'utf-8',
    indent: int = 4,
    backup: bool = True,
    encrypt_key: Optional[bytes] = None,
    set_permissions: Optional[int] = None
) -> bool:
    """
    Write JSON to file with optional backup, encryption, permissions.

    Args:
        file_path: JSON file path
        data: Data to write
        encoding: File encoding
        indent: Pretty print indent
        backup: Create backup before overwrite
        encrypt_key: Optional encryption key bytes
        set_permissions: Optional file permission mode

    Returns:
        True if success else False
    """
    content = json.dumps(data, indent=indent)
    return write_file(file_path, content, encoding, backup, encrypt_key, set_permissions)

# Alias functions for test compatibility (used in test_file_ops.py)

def write_json_file(*args, **kwargs):
    return write_json(*args, **kwargs)

def read_json_file(*args, **kwargs):
    return read_json(*args, **kwargs)

def write_text_file(*args, **kwargs):
    return write_file(*args, **kwargs)

def read_text_file(*args, **kwargs):
    return read_file(*args, **kwargs)
