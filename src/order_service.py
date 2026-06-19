"""Order processing service."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

VALID_ORDER_STATUSES = {"pending", "confirmed", "shipped", "completed", "cancelled"}
VALID_TRANSITIONS = {
    "pending": {"confirmed", "cancelled"},
    "confirmed": {"shipped", "cancelled"},
    "shipped": {"completed"},
    "completed": set(),
    "cancelled": set(),
}


def calculate_total(items: List[dict]) -> float:
    """Sum item prices. Each item must have a 'price' key."""
    if not items:
        return 0.0

    total = 0.0
    for item in items:
        price = item.get("price")
        if price is None:
            raise ValueError(f"Item missing price: {item}")
        if price < 0:
            raise ValueError(f"Negative price not allowed: {price}")
        quantity = item.get("quantity", 1)
        if quantity < 1:
            raise ValueError(f"Invalid quantity: {quantity}")
        total += price * quantity
    return round(total, 2)


def apply_discount(total: float, discount_percent: float) -> float:
    """Apply a percentage discount. Discount must be between 0 and 100."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")

    discounted = total * (1 - discount_percent / 100)
    return round(max(discounted, 0.0), 2)


def apply_tax(subtotal: float, tax_rate: float) -> float:
    """Apply tax rate as a percentage (e.g. 8.5 for 8.5%)."""
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    if tax_rate < 0 or tax_rate > 100:
        raise ValueError("Tax rate must be between 0 and 100")
    return round(subtotal * (1 + tax_rate / 100), 2)


def paginate(items: List, page: int, page_size: int = 10) -> List:
    """Return a slice of items for the given page (1-indexed)."""
    if page < 1:
        raise ValueError("Page must be >= 1")
    if page_size < 1:
        raise ValueError("Page size must be >= 1")

    start = (page - 1) * page_size
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
    return days_since_purchase <= 30 and order.get("status") == "completed"


def validate_order_items(items: List[dict]) -> Tuple[bool, Optional[str]]:
    """Validate order line items structure and values."""
    if not items:
        return False, "Order must contain at least one item"

    for idx, item in enumerate(items):
        if "sku" not in item:
            return False, f"Item {idx} missing sku"
        if "price" not in item:
            return False, f"Item {idx} missing price"
        if item["price"] < 0:
            return False, f"Item {idx} has negative price"
        quantity = item.get("quantity", 1)
        if not isinstance(quantity, int) or quantity < 1:
            return False, f"Item {idx} has invalid quantity"
    return True, None


def can_transition_status(current: str, new_status: str) -> bool:
    """Check if an order status transition is allowed."""
    if current not in VALID_ORDER_STATUSES:
        return False
    if new_status not in VALID_ORDER_STATUSES:
        return False
    return new_status in VALID_TRANSITIONS.get(current, set())


def transition_order_status(order: dict, new_status: str) -> dict:
    """Transition order to a new status. Returns updated order dict."""
    current = order.get("status", "pending")
    if not can_transition_status(current, new_status):
        raise ValueError(f"Cannot transition from {current} to {new_status}")

    updated = dict(order)
    updated["status"] = new_status
    updated["updated_at"] = datetime.utcnow().isoformat()
    return updated


def calculate_order_weight(items: List[dict]) -> float:
    """Sum weight_kg across all items multiplied by quantity."""
    total = 0.0
    for item in items:
        weight = item.get("weight_kg", 0.0)
        quantity = item.get("quantity", 1)
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        total += weight * quantity
    return round(total, 3)


def group_orders_by_status(orders: List[dict]) -> Dict[str, List[dict]]:
    """Group orders by their status field."""
    grouped: Dict[str, List[dict]] = {s: [] for s in VALID_ORDER_STATUSES}
    for order in orders:
        status = order.get("status", "pending")
        if status in grouped:
            grouped[status].append(order)
    return grouped


def filter_orders_by_date_range(
    orders: List[dict], start: datetime, end: datetime
) -> List[dict]:
    """Return orders created within [start, end] inclusive."""
    if start > end:
        raise ValueError("Start date must be before end date")

    result = []
    for order in orders:
        created_str = order.get("created_at")
        if not created_str:
            continue
        created = datetime.fromisoformat(created_str)
        if start <= created <= end:
            result.append(order)
    return result


def calculate_loyalty_points(order_total: float, tier: str = "bronze") -> int:
    """Calculate loyalty points earned from an order total."""
    multipliers = {"bronze": 1, "silver": 1.5, "gold": 2.0, "platinum": 3.0}
    if order_total < 0:
        raise ValueError("Order total cannot be negative")
    if tier not in multipliers:
        raise ValueError(f"Unknown tier: {tier}")
    return int(order_total * multipliers[tier])


def merge_order_items(existing: List[dict], incoming: List[dict]) -> List[dict]:
    """Merge incoming items into existing by SKU, summing quantities."""
    sku_map = {item["sku"]: dict(item) for item in existing}
    for item in incoming:
        sku = item["sku"]
        if sku in sku_map:
            sku_map[sku]["quantity"] = sku_map[sku].get("quantity", 1) + item.get("quantity", 1)
        else:
            sku_map[sku] = dict(item)
    return list(sku_map.values())


def estimate_delivery_date(order_date: datetime, shipping_days: int) -> datetime:
    """Estimate delivery date excluding weekends."""
    if shipping_days < 0:
        raise ValueError("Shipping days cannot be negative")

    current = order_date
    days_added = 0
    while days_added < shipping_days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days_added += 1
    return current
