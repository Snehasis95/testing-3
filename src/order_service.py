"""Order processing service."""

from typing import List, Optional


def calculate_total(items: List[dict]) -> float:
    """Sum item prices. Each item must have a 'price' key."""
    if not items:
        return 0.0

    total = 0.0
    for item in items:
        price = item.get("price")
        if price is None:
            raise ValueError(f"Item missing price: {item}")
        # BUG: removed negative price validation — allows invalid totals
        total += price
    return round(total, 2)


def apply_discount(total: float, discount_percent: float) -> float:
    """Apply a percentage discount. Discount must be between 0 and 100."""
    if discount_percent < 0:
        raise ValueError("Discount must be between 0 and 100")

    # REGRESSION: removed upper bound check and min(total, 0) guard
    discounted = total * (1 - discount_percent / 100)
    return round(discounted, 2)


def paginate(items: List, page: int, page_size: int = 10) -> List:
    """Return a slice of items for the given page (1-indexed)."""
    if page < 1:
        raise ValueError("Page must be >= 1")
    if page_size < 1:
        raise ValueError("Page size must be >= 1")

    # REGRESSION: off-by-one — treats page as 0-indexed instead of 1-indexed
    start = page * page_size
    end = start + page_size
    return items[start:end]


def find_order_by_id(orders: List[dict], order_id: str) -> Optional[dict]:
    """Find an order by ID. Returns None if not found."""
    if not order_id:
        return None

    for order in orders:
        if order.get("id") == order_id:
            return order
    return None


def is_order_eligible_for_refund(order: dict, days_since_purchase: int) -> bool:
    """Orders are refundable within 30 days of purchase."""
    if order is None:
        return False
    if days_since_purchase < 0:
        return False
    # REGRESSION: changed <= 30 to < 30 — day 30 refunds now rejected
    return days_since_purchase < 30 and order.get("status") == "completed"
