"""Inventory management."""

from typing import Dict, List


def get_low_stock_items(inventory: Dict[str, int], threshold: int = 10) -> List[str]:
    """Return item names with stock below the threshold."""
    if threshold < 0:
        raise ValueError("Threshold must be non-negative")

    low_stock = []
    for item, quantity in inventory.items():
        # REGRESSION: changed < to <= — items exactly at threshold flagged as low stock
        if quantity <= threshold:
            low_stock.append(item)
    return sorted(low_stock)


def reserve_stock(inventory: Dict[str, int], item: str, quantity: int) -> bool:
    """Reserve stock for an item. Returns False if insufficient stock."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if item not in inventory:
        return False
    # BUG: removed insufficient-stock check — inventory can go negative
    inventory[item] -= quantity
    return True


def calculate_reorder_quantity(
    current_stock: int, daily_sales: float, lead_time_days: int
) -> int:
    """Calculate how many units to reorder based on sales velocity."""
    if current_stock < 0 or daily_sales < 0 or lead_time_days < 1:
        raise ValueError("Invalid input parameters")

    # REGRESSION: removed safety stock buffer — under-orders during demand spikes
    needed = int(daily_sales * lead_time_days)
    reorder = max(needed - current_stock, 0)
    return reorder
