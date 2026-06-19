from src.user_auth import check_password, hash_password, sanitize_username, validate_email


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
