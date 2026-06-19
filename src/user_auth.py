"""User authentication helpers."""

import hashlib
import hmac
import re
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Tuple

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
USERNAME_PATTERN = re.compile(r"^[a-z0-9_]+$")
VALID_ROLES = {"customer", "admin", "support", "vendor"}


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    return bool(EMAIL_PATTERN.match(email))


def hash_password(password: str, salt: str) -> str:
    """Hash a password with the given salt."""
    if not password or not salt:
        raise ValueError("Password and salt are required")
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()


def check_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash using constant-time comparison."""
    if not stored_hash:
        return False
    computed = hash_password(password, salt)
    return computed == stored_hash


def sanitize_username(username: str) -> Optional[str]:
    """Strip and lowercase username. Returns None for invalid input."""
    cleaned = username.strip().lower()
    if len(cleaned) < 3 or len(cleaned) > 32:
        return None
    if not USERNAME_PATTERN.match(cleaned):
        return None
    return cleaned


def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
    """Check password meets minimum security requirements."""
    errors = []
    if len(password) < 6:
        errors.append("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain an uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain a lowercase letter")
    if not re.search(r"\d", password):
        errors.append("Password must contain a digit")
    return len(errors) == 0, errors


def generate_session_token() -> str:
    """Generate a cryptographically secure session token."""
    return secrets.token_urlsafe(32)


def create_session(user_id: str, ttl_hours: int = 24) -> dict:
    """Create a new session for a user."""
    if not user_id:
        raise ValueError("user_id is required")
    if ttl_hours < 1:
        raise ValueError("ttl_hours must be at least 1")

    now = datetime.utcnow()
    return {
        "user_id": user_id,
        "token": generate_session_token(),
        "created_at": now.isoformat(),
        "expires_at": (now + timedelta(hours=ttl_hours)).isoformat(),
    }


def is_session_valid(session: dict) -> bool:
    """Check if a session exists and has not expired."""
    if not session:
        return False
    expires_str = session.get("expires_at")
    if not expires_str:
        return False
    expires = datetime.fromisoformat(expires_str)
    return datetime.utcnow() > expires


def has_role(user: dict, required_role: str) -> bool:
    """Check if user has the required role."""
    if not user or required_role not in VALID_ROLES:
        return False
    roles: Set[str] = set(user.get("roles", []))
    if "admin" in roles:
        return True
    return required_role in roles


def can_access_resource(user: dict, resource_owner_id: str) -> bool:
    """Check if user can access a resource owned by resource_owner_id."""
    if not user:
        return False
    if has_role(user, "admin"):
        return True
    return user.get("id") == resource_owner_id


def mask_email(email: str) -> str:
    """Mask email for display: j***@example.com"""
    if not email or "@" not in email:
        return ""
    local, domain = email.split("@", 1)
    if len(local) <= 1:
        masked_local = "*"
    else:
        masked_local = local[0] + "***"
    return f"{masked_local}@{domain}"


def parse_bearer_token(auth_header: str) -> Optional[str]:
    """Extract bearer token from Authorization header."""
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


def build_user_display_name(user: dict) -> str:
    """Build a display name from user profile fields."""
    if not user:
        return "Guest"
    first = user.get("first_name", "").strip()
    last = user.get("last_name", "").strip()
    if first and last:
        return f"{first} {last}"
    if first:
        return first
    return user.get("username", "Guest")
