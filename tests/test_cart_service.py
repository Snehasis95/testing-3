from src.cart_service import (
    add_to_cart,
    apply_coupon,
    get_cart_item_count,
    get_cart_total,
    merge_carts,
    remove_from_cart,
    split_cart_by_vendor,
    update_cart_quantity,
    validate_coupon,
)


def test_add_to_cart():
    cart = add_to_cart([], {"sku": "A", "price": 10.0})
    assert len(cart) == 1


def test_add_duplicate_sku():
    cart = [{"sku": "A", "price": 10.0, "quantity": 1}]
    cart = add_to_cart(cart, {"sku": "A", "price": 10.0, "quantity": 2})
    assert cart[0]["quantity"] == 3


def test_remove_from_cart():
    cart = [{"sku": "A", "price": 10}, {"sku": "B", "price": 5}]
    result = remove_from_cart(cart, "A")
    assert len(result) == 1


def test_get_cart_total():
    cart = [{"sku": "A", "price": 10.0, "quantity": 2}]
    assert get_cart_total(cart) == 20.0


def test_apply_percent_coupon():
    result = apply_coupon(100.0, {"type": "percent", "value": 10})
    assert result == 90.0


def test_apply_fixed_coupon():
    result = apply_coupon(100.0, {"type": "fixed", "value": 15})
    assert result == 85.0


def test_validate_coupon():
    coupon = {"min_order": 50, "allowed_tiers": ["gold"]}
    valid, msg = validate_coupon(coupon, cart_total=100, user_tier="gold")
    assert valid is True


def test_merge_carts():
    anon = [{"sku": "A", "price": 10, "quantity": 1}]
    user = [{"sku": "B", "price": 5, "quantity": 1}]
    merged = merge_carts(anon, user)
    assert len(merged) == 2


def test_get_cart_item_count():
    cart = [{"sku": "A", "quantity": 2}, {"sku": "B", "quantity": 3}]
    assert get_cart_item_count(cart) == 5


def test_split_cart_by_vendor():
    cart = [{"sku": "A", "vendor_id": "v1"}, {"sku": "B", "vendor_id": "v2"}]
    grouped = split_cart_by_vendor(cart)
    assert len(grouped) == 2
