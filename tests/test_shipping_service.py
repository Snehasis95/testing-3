from src.shipping_service import (
    calculate_dimensional_weight,
    calculate_shipping_cost,
    estimate_delivery_days,
    get_billable_weight,
    get_shipping_zone,
    is_free_shipping_eligible,
    validate_shipping_address,
)


def test_get_shipping_zone():
    assert get_shipping_zone("US") == "domestic"
    assert get_shipping_zone("CA") == "regional"
    assert get_shipping_zone("GB") == "international"


def test_calculate_shipping_cost():
    cost = calculate_shipping_cost(50.0, 2.0, "US")
    assert cost > 0


def test_free_shipping():
    cost = calculate_shipping_cost(100.0, 2.0, "US")
    assert cost == 0.0


def test_estimate_delivery_days():
    assert estimate_delivery_days("domestic") == 3
    assert estimate_delivery_days("domestic", express=True) == 1


def test_is_free_shipping_eligible():
    assert is_free_shipping_eligible(80.0) is True
    assert is_free_shipping_eligible(50.0) is False


def test_calculate_dimensional_weight():
    weight = calculate_dimensional_weight(50, 40, 30)
    assert weight == 12.0


def test_get_billable_weight():
    assert get_billable_weight(5.0, 8.0) == 8.0


def test_validate_shipping_address():
    address = {"line1": "123 Main", "city": "NYC", "postal_code": "10001", "country_code": "US"}
    valid, err = validate_shipping_address(address)
    assert valid is True
