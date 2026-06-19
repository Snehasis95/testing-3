"""Inventory management."""

from datetime import date, datetime
from typing import Dict, List, Optional, Tuple


def get_low_stock_items(inventory: Dict[str, int], threshold: int = 10) -> List[str]:
    """Return item names with stock below the threshold."""
    if threshold < 0:
        raise ValueError("Threshold must be non-negative")

    low_stock = []
    for item, quantity in inventory.items():
        if quantity < threshold:
            low_stock.append(item)
    return sorted(low_stock)


def reserve_stock(inventory: Dict[str, int], item: str, quantity: int) -> bool:
    """Reserve stock for an item. Returns False if insufficient stock."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if item not in inventory:
        return False
    if inventory[item] < quantity:
        return False

    inventory[item] -= quantity
    return True


def calculate_reorder_quantity(
    current_stock: int, daily_sales: float, lead_time_days: int
) -> int:
    """Calculate how many units to reorder based on sales velocity."""
    if current_stock < 0 or daily_sales < 0 or lead_time_days < 1:
        raise ValueError("Invalid input parameters")

    safety_stock = int(daily_sales * 2)
    needed = int(daily_sales * lead_time_days) + safety_stock
    reorder = max(needed - current_stock, 0)
    return reorder


def release_stock(inventory: Dict[str, int], item: str, quantity: int) -> None:
    """Return reserved stock back to inventory."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if item not in inventory:
        raise ValueError(f"Unknown item: {item}")
    inventory[item] += quantity


def batch_reserve_stock(
    inventory: Dict[str, int], reservations: Dict[str, int]
) -> Tuple[bool, Optional[str]]:
    """Reserve multiple items atomically. Rolls back on failure."""
    if not reservations:
        return True, None

    snapshot = dict(inventory)
    for item, quantity in reservations.items():
        if quantity <= 0:
            return False, f"Invalid quantity for {item}"
        if item not in inventory or inventory[item] < quantity:
            inventory.clear()
            inventory.update(snapshot)
            return False, f"Insufficient stock for {item}"
        inventory[item] -= quantity
    return True, None


def calculate_inventory_value(
    inventory: Dict[str, int], unit_prices: Dict[str, float]
) -> float:
    """Calculate total inventory value."""
    total = 0.0
    for item, quantity in inventory.items():
        if quantity < 0:
            raise ValueError(f"Negative stock for {item}")
        price = unit_prices.get(item, 0.0)
        if price < 0:
            raise ValueError(f"Negative price for {item}")
        total += quantity * price
    return round(total, 2)


def get_expiring_items(
    expiry_dates: Dict[str, date], within_days: int = 7
) -> List[str]:
    """Return items expiring within the given number of days."""
    if within_days < 0:
        raise ValueError("within_days cannot be negative")

    today = date.today()
    cutoff = today.toordinal() + within_days
    expiring = []
    for item, expiry in expiry_dates.items():
        if expiry.toordinal() <= cutoff:
            expiring.append(item)
    return sorted(expiring)


def allocate_to_warehouses(
    total_quantity: int, warehouses: Dict[str, int]
) -> Dict[str, int]:
    """Distribute quantity across warehouses proportionally by capacity."""
    if total_quantity < 0:
        raise ValueError("total_quantity cannot be negative")
    if not warehouses:
        return {}

    total_capacity = sum(warehouses.values())
    if total_capacity == 0:
        raise ValueError("Total warehouse capacity is zero")

    allocation = {}
    remaining = total_quantity
    items = list(warehouses.items())
    for i, (name, capacity) in enumerate(items):
        if i == len(items) - 1:
            allocation[name] = remaining
        else:
            share = int(total_quantity * capacity / total_capacity)
            allocation[name] = share
            remaining -= share
    return allocation


def transfer_stock(
    inventory: Dict[str, int],
    from_warehouse: str,
    to_warehouse: str,
    item: str,
    quantity: int,
) -> bool:
    """Transfer stock between two warehouse inventories."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    from_key = f"{from_warehouse}:{item}"
    to_key = f"{to_warehouse}:{item}"

    if from_key not in inventory or inventory[from_key] < quantity:
        return False

    inventory[from_key] -= quantity
    inventory[to_key] = inventory.get(to_key, 0) + quantity
    return True


def calculate_turnover_rate(
    units_sold: int, average_inventory: float, period_days: int
) -> float:
    """Calculate inventory turnover rate for a period."""
    if period_days < 1:
        raise ValueError("period_days must be at least 1")
    if average_inventory <= 0:
        raise ValueError("average_inventory must be positive")
    if units_sold < 0:
        raise ValueError("units_sold cannot be negative")

    annualized_sales = units_sold * (365 / period_days)
    return round(annualized_sales / average_inventory, 2)
