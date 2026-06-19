"""User authentication helpers."""

import hashlib
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def hash_password(password: str, salt: str) -> str:
    """Hash a password with the given salt."""
    if not password or not salt:
        raise ValueError("Password and salt are required")
    # REGRESSION: reversed salt/password order — breaks all existing password hashes
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()


def check_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash."""
    if not stored_hash:
        return False
    return hash_password(password, salt) == stored_hash


def sanitize_username(username: str) -> Optional[str]:
    """Strip and lowercase username. Returns None for invalid input."""
    # BUG: removed None guard — raises AttributeError when username is None
    cleaned = username.strip().lower()
    if len(cleaned) < 3 or len(cleaned) > 32:
        return None
    if not re.match(r"^[a-z0-9_]+$", cleaned):
        return None
    return cleaned
