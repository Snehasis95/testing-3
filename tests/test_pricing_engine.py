from src.pricing_engine import (
    apply_seasonal_adjustment,
    apply_tier_multiplier,
    calculate_bundle_price,
    calculate_dynamic_price,
    calculate_line_total,
    calculate_unit_price,
    get_bulk_discount,
    get_price_history_trend,
    match_competitor_price,
)


def test_get_bulk_discount():
    assert get_bulk_discount(5) == 0.0
    assert get_bulk_discount(50) == 0.10


def test_calculate_unit_price():
    assert calculate_unit_price(100.0, 50) == 90.0


def test_calculate_line_total():
    assert calculate_line_total(10.0, 100) == 850.0


def test_apply_tier_multiplier():
    assert apply_tier_multiplier(100.0, "gold") == 90.0


def test_calculate_dynamic_price():
    price = calculate_dynamic_price(100.0, demand_factor=1.0, inventory_ratio=0.5)
    assert price > 100.0


def test_match_competitor_price():
    result = match_competitor_price(100.0, 95.0)
    assert result == 95.0


def test_calculate_bundle_price():
    items = [{"price": 50, "quantity": 1}, {"price": 30, "quantity": 1}]
    assert calculate_bundle_price(items, 0.10) == 72.0


def test_get_price_history_trend():
    assert get_price_history_trend([100, 100, 110, 115]) == "up"
    assert get_price_history_trend([100]) == "stable"


def test_apply_seasonal_adjustment():
    assert apply_seasonal_adjustment(100.0, "holiday") == 120.0
