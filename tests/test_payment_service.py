from src.payment_service import (
    aggregate_payments_by_method,
    calculate_partial_refund,
    calculate_processing_fee,
    can_refund_payment,
    convert_currency,
    create_payment_record,
    format_currency,
    split_payment,
    validate_card_number,
    validate_payment_amount,
)


def test_validate_payment_amount():
    assert validate_payment_amount(50.0, "USD") is True
    assert validate_payment_amount(-1, "USD") is False


def test_calculate_processing_fee():
    fee = calculate_processing_fee(100.0, "card")
    assert fee == 3.20


def test_format_currency():
    assert format_currency(1234.5, "USD") == "$1,234.50"


def test_create_payment_record():
    record = create_payment_record("ord-1", 99.99, "USD", "card")
    assert record["status"] == "pending"


def test_can_refund_payment():
    payment = {"status": "completed"}
    assert can_refund_payment(payment, 30) is True
    assert can_refund_payment(payment, 91) is False


def test_calculate_partial_refund():
    assert calculate_partial_refund(100.0, 50) == 50.0


def test_split_payment():
    parts = split_payment(100.0, 3)
    assert sum(parts) == 100.0


def test_convert_currency():
    rates = {"USD": 1.0, "EUR": 0.85}
    result = convert_currency(100.0, "USD", "EUR", rates)
    assert result == 85.0


def test_aggregate_payments():
    payments = [
        {"status": "completed", "method": "card", "amount": 50},
        {"status": "completed", "method": "card", "amount": 30},
    ]
    totals = aggregate_payments_by_method(payments)
    assert totals["card"] == 80.0


def test_validate_card_number():
    assert validate_card_number("4532015112830366") is True
    assert validate_card_number("1234") is False
