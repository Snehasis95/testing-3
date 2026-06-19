import pytest
from datetime import datetime, timedelta

from src.order_service import (
    apply_discount,
    apply_tax,
    calculate_loyalty_points,
    calculate_order_weight,
    calculate_total,
    can_transition_status,
    estimate_delivery_date,
    filter_orders_by_date_range,
    find_order_by_id,
    is_order_eligible_for_refund,
    merge_order_items,
    paginate,
    transition_order_status,
    validate_order_items,
)


def test_calculate_total():
    items = [{"price": 10.0, "quantity": 2}, {"price": 20.5}]
    assert calculate_total(items) == 40.5


def test_calculate_total_empty():
    assert calculate_total([]) == 0.0


def test_apply_discount():
    assert apply_discount(100.0, 10) == 90.0


def test_apply_tax():
    assert apply_tax(100.0, 8.5) == 108.5


def test_paginate_first_page():
    items = list(range(25))
    assert paginate(items, page=1, page_size=10) == list(range(10))


def test_paginate_second_page():
    items = list(range(25))
    assert paginate(items, page=2, page_size=10) == list(range(10, 20))


def test_find_order_by_id():
    orders = [{"id": "a1", "status": "completed"}, {"id": "b2", "status": "pending"}]
    assert find_order_by_id(orders, "b2") == {"id": "b2", "status": "pending"}


def test_refund_eligible():
    order = {"id": "x", "status": "completed"}
    assert is_order_eligible_for_refund(order, 15) is True


def test_refund_eligible_day_30():
    order = {"id": "x", "status": "completed"}
    assert is_order_eligible_for_refund(order, 30) is True


def test_refund_not_eligible_after_30_days():
    order = {"id": "x", "status": "completed"}
    assert is_order_eligible_for_refund(order, 31) is False


def test_validate_order_items():
    valid, err = validate_order_items([{"sku": "A1", "price": 10.0}])
    assert valid is True
    assert err is None


def test_can_transition_status():
    assert can_transition_status("pending", "confirmed") is True
    assert can_transition_status("completed", "pending") is False


def test_transition_order_status():
    order = {"id": "1", "status": "pending"}
    updated = transition_order_status(order, "confirmed")
    assert updated["status"] == "confirmed"


def test_calculate_order_weight():
    items = [{"weight_kg": 1.5, "quantity": 2}, {"weight_kg": 0.5}]
    assert calculate_order_weight(items) == 3.5


def test_merge_order_items():
    existing = [{"sku": "A", "price": 10, "quantity": 1}]
    incoming = [{"sku": "A", "price": 10, "quantity": 2}]
    merged = merge_order_items(existing, incoming)
    assert merged[0]["quantity"] == 3


def test_calculate_loyalty_points():
    assert calculate_loyalty_points(100.0, "gold") == 200


def test_estimate_delivery_date():
    monday = datetime(2024, 1, 1)
    result = estimate_delivery_date(monday, 3)
    assert result.weekday() < 5


def test_filter_orders_by_date_range():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 31)
    orders = [{"id": "1", "created_at": "2024-01-15T10:00:00"}]
    result = filter_orders_by_date_range(orders, start, end)
    assert len(result) == 1
