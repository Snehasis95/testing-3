"""Database query helpers with parameterized queries."""

from typing import Any, List, Optional, Tuple


def search_users_by_name(conn: Any, name: str) -> List[dict]:
    """Search users by display name using parameterized query."""
    query = "SELECT * FROM users WHERE name = ?"
    cursor = conn.execute(query, (name,))
    return cursor.fetchall()


def get_order_by_id(conn: Any, order_id: str) -> Optional[dict]:
    """Fetch a single order by ID."""
    query = "SELECT * FROM orders WHERE id = ?"
    cursor = conn.execute(query, (order_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_orders_by_user(conn: Any, user_id: str, limit: int = 50) -> List[dict]:
    """Fetch orders for a user with limit."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    query = "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT ?"
    cursor = conn.execute(query, (user_id, limit))
    return cursor.fetchall()


def update_order_status(conn: Any, order_id: str, status: str) -> int:
    """Update order status. Returns rows affected."""
    query = "UPDATE orders SET status = ?, updated_at = datetime('now') WHERE id = ?"
    cursor = conn.execute(query, (status, order_id))
    conn.commit()
    return cursor.rowcount


def search_products(
    conn: Any, keyword: str, category: Optional[str] = None
) -> List[dict]:
    """Search products by keyword with optional category filter."""
    if category:
        query = "SELECT * FROM products WHERE name LIKE ? AND category = ?"
        params: Tuple = (f"%{keyword}%", category)
    else:
        query = "SELECT * FROM products WHERE name LIKE ?"
        params = (f"%{keyword}%",)
    cursor = conn.execute(query, params)
    return cursor.fetchall()


def get_inventory_levels(conn: Any, warehouse_id: str) -> List[dict]:
    """Get inventory levels for a warehouse."""
    query = "SELECT * FROM inventory WHERE warehouse_id = ?"
    cursor = conn.execute(query, (warehouse_id,))
    return cursor.fetchall()


def insert_audit_log(conn: Any, user_id: str, action: str, details: str) -> None:
    """Insert an audit log entry."""
    query = "INSERT INTO audit_log (user_id, action, details, created_at) VALUES (?, ?, ?, datetime('now'))"
    conn.execute(query, (user_id, action, details))
    conn.commit()
