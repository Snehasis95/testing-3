import pytest

from src.order_service import (
    apply_discount,
    calculate_total,
    find_order_by_id,
    is_order_eligible_for_refund,
    paginate,
)


def test_calculate_total():
    items = [{"price": 10.0}, {"price": 20.5}]
    assert calculate_total(items) == 30.5


def test_calculate_total_empty():
    assert calculate_total([]) == 0.0


def test_apply_discount():
    assert apply_discount(100.0, 10) == 90.0


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


def test_refund_not_eligible_after_30_days():
    order = {"id": "x", "status": "completed"}
    assert is_order_eligible_for_refund(order, 31) is False
