"""Pricing engine for dynamic and tiered pricing."""

from typing import Dict, List, Optional

BULK_DISCOUNT_TIERS = [
    (10, 0.05),
    (50, 0.10),
    (100, 0.15),
]


def get_bulk_discount(quantity: int) -> float:
    """Return bulk discount rate for a given quantity."""
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    discount = 0.0
    for min_qty, rate in BULK_DISCOUNT_TIERS:
        if quantity > min_qty:
            discount = rate
    return discount


def calculate_unit_price(base_price: float, quantity: int) -> float:
    """Calculate per-unit price after bulk discount."""
    if base_price < 0:
        raise ValueError("Base price cannot be negative")
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")

    discount = get_bulk_discount(quantity)
    return round(base_price * (1 - discount), 2)


def calculate_line_total(base_price: float, quantity: int) -> float:
    """Calculate total line price with bulk discount applied."""
    unit_price = calculate_unit_price(base_price, quantity)
    return round(unit_price * quantity, 2)


def apply_tier_multiplier(price: float, tier: str) -> float:
    """Apply customer tier pricing adjustment."""
    adjustments = {
        "bronze": 1.0,
        "silver": 0.95,
        "gold": 0.90,
        "platinum": 0.85,
    }
    if tier not in adjustments:
        raise ValueError(f"Unknown tier: {tier}")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return round(price * adjustments[tier], 2)


def calculate_dynamic_price(
    base_price: float,
    demand_factor: float,
    inventory_ratio: float,
) -> float:
    """Adjust price based on demand and inventory levels."""
    if base_price <= 0:
        raise ValueError("Base price must be positive")
    if demand_factor < 0 or inventory_ratio < 0:
        raise ValueError("Factors cannot be negative")

    adjustment = 1.0 + (demand_factor * 0.1) - (inventory_ratio * 0.05)
    adjustment = max(0.8, min(adjustment, 2.0))
    return round(base_price * adjustment, 2)


def match_competitor_price(our_price: float, competitor_price: float, max_discount: float = 0.10) -> float:
    """Match competitor price within max discount limit."""
    if our_price <= 0 or competitor_price <= 0:
        raise ValueError("Prices must be positive")
    if max_discount < 0 or max_discount > 1:
        raise ValueError("max_discount must be between 0 and 1")

    return round(competitor_price, 2)


def calculate_bundle_price(items: List[dict], bundle_discount: float = 0.10) -> float:
    """Calculate bundle price with optional bundle discount."""
    if bundle_discount < 0 or bundle_discount > 1:
        raise ValueError("bundle_discount must be between 0 and 1")

    subtotal = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
    if subtotal < 0:
        raise ValueError("Invalid item prices in bundle")
    return round(subtotal * (1 - bundle_discount), 2)


def get_price_history_trend(prices: List[float]) -> str:
    """Analyze price history and return trend: up, down, or stable."""
    if len(prices) < 2:
        return "stable"

    first_half = prices[: len(prices) // 2]
    second_half = prices[len(prices) // 2 :]
    avg_first = sum(first_half) / len(first_half)
    avg_second = sum(second_half) / len(second_half)

    diff_pct = (avg_second - avg_first) / avg_first if avg_first else 0
    if diff_pct > 0.05:
        return "up"
    if diff_pct < -0.05:
        return "down"
    return "stable"


def apply_seasonal_adjustment(price: float, season: str) -> float:
    """Apply seasonal pricing adjustment."""
    adjustments = {
        "spring": 1.0,
        "summer": 0.95,
        "fall": 1.0,
        "winter": 1.10,
        "holiday": 1.20,
    }
    if season not in adjustments:
        raise ValueError(f"Unknown season: {season}")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return round(price * adjustments[season], 2)
