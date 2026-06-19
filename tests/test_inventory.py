from datetime import date, timedelta

from src.inventory import (
    allocate_to_warehouses,
    batch_reserve_stock,
    calculate_inventory_value,
    calculate_reorder_quantity,
    calculate_turnover_rate,
    get_expiring_items,
    get_low_stock_items,
    release_stock,
    reserve_stock,
    transfer_stock,
)


def test_get_low_stock_items():
    inventory = {"apple": 5, "banana": 20, "cherry": 3}
    assert get_low_stock_items(inventory, threshold=10) == ["apple", "cherry"]


def test_reserve_stock():
    inventory = {"apple": 10}
    assert reserve_stock(inventory, "apple", 3) is True
    assert inventory["apple"] == 7


def test_calculate_reorder_quantity():
    assert calculate_reorder_quantity(current_stock=5, daily_sales=10, lead_time_days=7) == 85


def test_release_stock():
    inventory = {"apple": 5}
    release_stock(inventory, "apple", 3)
    assert inventory["apple"] == 8


def test_batch_reserve_stock():
    inventory = {"apple": 10, "banana": 5}
    ok, err = batch_reserve_stock(inventory, {"apple": 3, "banana": 2})
    assert ok is True
    assert inventory["apple"] == 7


def test_calculate_inventory_value():
    inventory = {"apple": 10, "banana": 5}
    prices = {"apple": 1.0, "banana": 2.0}
    assert calculate_inventory_value(inventory, prices) == 20.0


def test_get_expiring_items():
    today = date.today()
    soon = today + timedelta(days=3)
    later = today + timedelta(days=30)
    expiry_dates = {"milk": soon, "rice": later}
    assert "milk" in get_expiring_items(expiry_dates, within_days=7)


def test_allocate_to_warehouses():
    warehouses = {"east": 60, "west": 40}
    result = allocate_to_warehouses(100, warehouses)
    assert sum(result.values()) == 100


def test_transfer_stock():
    inventory = {"wh1:apple": 10, "wh2:apple": 0}
    assert transfer_stock(inventory, "wh1", "wh2", "apple", 4) is True
    assert inventory["wh1:apple"] == 6
    assert inventory["wh2:apple"] == 4


def test_calculate_turnover_rate():
    rate = calculate_turnover_rate(units_sold=365, average_inventory=100, period_days=365)
    assert rate == 3.65
