from datetime import datetime, timedelta

from src.user_auth import (
    build_user_display_name,
    can_access_resource,
    check_password,
    create_session,
    has_role,
    hash_password,
    is_session_valid,
    mask_email,
    parse_bearer_token,
    sanitize_username,
    validate_email,
    validate_password_strength,
)


def test_validate_email():
    assert validate_email("user@example.com") is True
    assert validate_email("invalid") is False


def test_hash_and_check_password():
    salt = "randomsalt"
    hashed = hash_password("secret123", salt)
    assert check_password("secret123", salt, hashed) is True
    assert check_password("wrong", salt, hashed) is False


def test_sanitize_username():
    assert sanitize_username("  MyUser_1  ") == "myuser_1"
    assert sanitize_username("ab") is None
    assert sanitize_username(None) is None


def test_validate_password_strength():
    valid, errors = validate_password_strength("Weak1")
    assert valid is False
    valid, errors = validate_password_strength("StrongPass1")
    assert valid is True


def test_create_and_validate_session():
    session = create_session("user-123", ttl_hours=24)
    assert is_session_valid(session) is True


def test_expired_session():
    session = create_session("user-123", ttl_hours=1)
    session["expires_at"] = (datetime.utcnow() - timedelta(hours=1)).isoformat()
    assert is_session_valid(session) is False


def test_has_role():
    admin = {"id": "1", "roles": ["admin"]}
    customer = {"id": "2", "roles": ["customer"]}
    assert has_role(admin, "support") is True
    assert has_role(customer, "admin") is False


def test_can_access_resource():
    user = {"id": "u1", "roles": ["customer"]}
    assert can_access_resource(user, "u1") is True
    assert can_access_resource(user, "u2") is False


def test_mask_email():
    assert mask_email("john@example.com") == "j***@example.com"


def test_parse_bearer_token():
    assert parse_bearer_token("Bearer abc123") == "abc123"
    assert parse_bearer_token("Basic abc") is None


def test_build_user_display_name():
    user = {"first_name": "John", "last_name": "Doe"}
    assert build_user_display_name(user) == "John Doe"
