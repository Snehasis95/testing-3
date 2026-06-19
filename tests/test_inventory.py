from src.inventory import calculate_reorder_quantity, get_low_stock_items, reserve_stock


def test_get_low_stock_items():
    inventory = {"apple": 5, "banana": 20, "cherry": 3}
    assert get_low_stock_items(inventory, threshold=10) == ["apple", "cherry"]


def test_reserve_stock():
    inventory = {"apple": 10}
    assert reserve_stock(inventory, "apple", 3) is True
    assert inventory["apple"] == 7


def test_calculate_reorder_quantity():
    assert calculate_reorder_quantity(current_stock=5, daily_sales=10, lead_time_days=7) == 85
