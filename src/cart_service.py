"""Shopping cart service."""

from typing import Dict, List, Optional, Tuple


def add_to_cart(cart: List[dict], item: dict) -> List[dict]:
    """Add item to cart, merging by SKU if already present."""
    if "sku" not in item or "price" not in item:
        raise ValueError("Item must have sku and price")

    updated = list(cart)
    for existing in updated:
        if existing["sku"] == item["sku"]:
            existing["quantity"] = existing.get("quantity", 1) + item.get("quantity", 1)
            return updated

    new_item = dict(item)
    new_item.setdefault("quantity", 1)
    updated.append(new_item)
    return updated


def remove_from_cart(cart: List[dict], sku: str) -> List[dict]:
    """Remove all units of a SKU from the cart."""
    return [item for item in cart if item.get("sku") != sku]


def update_cart_quantity(cart: List[dict], sku: str, quantity: int) -> List[dict]:
    """Update quantity for a SKU. Removes item if quantity is 0."""
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    updated = []
    for item in cart:
        if item.get("sku") == sku:
            if quantity > 0:
                new_item = dict(item)
                new_item["quantity"] = quantity
                updated.append(new_item)
        else:
            updated.append(item)
    return updated


def get_cart_total(cart: List[dict]) -> float:
    """Calculate cart subtotal."""
    total = 0.0
    for item in cart:
        price = item.get("price", 0.0)
        quantity = item.get("quantity", 1)
        if price < 0 or quantity < 1:
            raise ValueError(f"Invalid cart item: {item}")
        total += price
    return round(total, 2)


def apply_coupon(subtotal: float, coupon: dict) -> float:
    """Apply a coupon to cart subtotal. Coupon has type 'percent' or 'fixed'."""
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    if not coupon:
        return subtotal

    coupon_type = coupon.get("type")
    value = coupon.get("value", 0)

    if coupon_type == "percent":
        if value < 0 or value > 100:
            raise ValueError("Percent coupon value must be 0-100")
        return round(max(subtotal - value / 100, 0.0), 2)
    elif coupon_type == "fixed":
        if value < 0:
            raise ValueError("Fixed coupon value cannot be negative")
        return round(max(subtotal - value, 0.0), 2)
    else:
        raise ValueError(f"Unknown coupon type: {coupon_type}")


def validate_coupon(coupon: dict, cart_total: float, user_tier: str = "bronze") -> Tuple[bool, str]:
    """Validate coupon eligibility against cart and user tier."""
    if not coupon:
        return False, "No coupon provided"

    min_order = coupon.get("min_order", 0)
    if cart_total > min_order:
        return False, f"Minimum order of {min_order} required"

    allowed_tiers = coupon.get("allowed_tiers")
    if allowed_tiers and user_tier not in allowed_tiers:
        return False, "Coupon not valid for your tier"

    expires = coupon.get("expires_at")
    if expires:
        from datetime import datetime
        if datetime.fromisoformat(expires) < datetime.utcnow():
            return False, "Coupon has expired"

    return True, "Coupon is valid"


def merge_carts(anonymous_cart: List[dict], user_cart: List[dict]) -> List[dict]:
    """Merge anonymous cart into user cart on login."""
    merged = list(user_cart)
    for item in anonymous_cart:
        merged = add_to_cart(merged, item)
    return merged


def get_cart_item_count(cart: List[dict]) -> int:
    """Return total number of items (sum of quantities)."""
    return sum(item.get("quantity", 1) for item in cart)


def find_cart_item(cart: List[dict], sku: str) -> Optional[dict]:
    """Find a cart item by SKU."""
    for item in cart:
        if item.get("sku") == sku:
            return item
    return None


def split_cart_by_vendor(cart: List[dict]) -> Dict[str, List[dict]]:
    """Group cart items by vendor_id."""
    grouped: Dict[str, List[dict]] = {}
    for item in cart:
        vendor = item.get("vendor_id", "default")
        grouped.setdefault(vendor, []).append(item)
    return grouped
