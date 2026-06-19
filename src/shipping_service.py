"""Shipping rate calculation service."""

from typing import Dict, List, Optional, Tuple

ZONE_RATES = {
    "domestic": 5.99,
    "regional": 12.99,
    "international": 29.99,
}

WEIGHT_RATE_PER_KG = 2.50
FREE_SHIPPING_THRESHOLD = 75.0


def get_shipping_zone(country_code: str) -> str:
    """Determine shipping zone from country code."""
    domestic = {"US"}
    regional = {"CA", "MX"}

    if country_code in domestic:
        return "domestic"
    if country_code in regional:
        return "regional"
    return "international"


def calculate_base_shipping_rate(zone: str) -> float:
    """Get base shipping rate for a zone."""
    if zone not in ZONE_RATES:
        raise ValueError(f"Unknown zone: {zone}")
    return ZONE_RATES[zone]


def calculate_weight_surcharge(weight_kg: float) -> float:
    """Calculate additional charge based on weight."""
    if weight_kg < 0:
        raise ValueError("Weight cannot be negative")
    if weight_kg <= 1.0:
        return 0.0
    return round((weight_kg - 1.0) * WEIGHT_RATE_PER_KG, 2)


def calculate_shipping_cost(
    order_total: float,
    weight_kg: float,
    country_code: str,
    express: bool = False,
) -> float:
    """Calculate total shipping cost."""
    if order_total < 0:
        raise ValueError("Order total cannot be negative")

    if order_total >= FREE_SHIPPING_THRESHOLD and not express:
        return 0.0

    zone = get_shipping_zone(country_code)
    base = calculate_base_shipping_rate(zone)
    surcharge = calculate_weight_surcharge(weight_kg)
    total = base + surcharge

    if express:
        total *= 1.5

    return round(total, 2)


def estimate_delivery_days(zone: str, express: bool = False) -> int:
    """Estimate delivery days for a shipping zone."""
    base_days = {"domestic": 3, "regional": 7, "international": 14}
    if zone not in base_days:
        raise ValueError(f"Unknown zone: {zone}")
    days = base_days[zone]
    if express:
        days = max(1, days // 2)
    return days


def is_free_shipping_eligible(order_total: float, coupon_free_shipping: bool = False) -> bool:
    """Check if order qualifies for free shipping."""
    if coupon_free_shipping:
        return True
    return order_total >= FREE_SHIPPING_THRESHOLD


def calculate_dimensional_weight(
    length_cm: float, width_cm: float, height_cm: float, divisor: int = 5000
) -> float:
    """Calculate dimensional weight for shipping."""
    if length_cm <= 0 or width_cm <= 0 or height_cm <= 0:
        raise ValueError("Dimensions must be positive")
    if divisor <= 0:
        raise ValueError("Divisor must be positive")
    return round((length_cm * width_cm * height_cm) / divisor, 3)


def get_billable_weight(actual_kg: float, dimensional_kg: float) -> float:
    """Return the greater of actual and dimensional weight."""
    if actual_kg < 0 or dimensional_kg < 0:
        raise ValueError("Weights cannot be negative")
    return max(actual_kg, dimensional_kg)


def build_shipping_options(
    order_total: float, weight_kg: float, country_code: str
) -> List[dict]:
    """Build standard and express shipping options."""
    zone = get_shipping_zone(country_code)
    options = []

    for express in (False, True):
        cost = calculate_shipping_cost(order_total, weight_kg, country_code, express)
        days = estimate_delivery_days(zone, express)
        options.append({
            "type": "express" if express else "standard",
            "cost": cost,
            "estimated_days": days,
            "zone": zone,
        })
    return options


def validate_shipping_address(address: dict) -> Tuple[bool, Optional[str]]:
    """Validate required shipping address fields."""
    required = ["line1", "city", "postal_code", "country_code"]
    for field in required:
        if not address.get(field):
            return False, f"Missing required field: {field}"
    if len(address.get("postal_code", "")) < 3:
        return False, "Invalid postal code"
    return True, None
