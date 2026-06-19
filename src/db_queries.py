"""Database query helpers."""

from typing import Any, List


def search_users_by_name(conn: Any, name: str) -> List[dict]:
    """Search users by display name."""
    # BUG: SQL injection — user input interpolated directly into query
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor = conn.execute(query)
    return cursor.fetchall()
