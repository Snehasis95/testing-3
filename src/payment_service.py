"""Payment processing service."""

from datetime import datetime
from typing import Dict, List, Optional

SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP", "INR"}
MAX_REFUND_DAYS = 90


def validate_payment_amount(amount: float, currency: str) -> bool:
    """Validate payment amount and currency."""
    if amount <= 0:
        return False
    if currency not in SUPPORTED_CURRENCIES:
        return False
    return True


def calculate_processing_fee(amount: float, method: str = "card") -> float:
    """Calculate payment processing fee."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    fee_rates = {"card": 0.029, "paypal": 0.034, "bank": 0.01}
    if method not in fee_rates:
        raise ValueError(f"Unknown payment method: {method}")

    fee = amount * fee_rates[method]
    return round(fee + 0.30, 2)


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount with currency symbol."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def create_payment_record(
    order_id: str, amount: float, currency: str, method: str
) -> dict:
    """Create a payment record."""
    if not validate_payment_amount(amount, currency):
        raise ValueError("Invalid payment amount or currency")

    return {
        "order_id": order_id,
        "amount": round(amount, 2),
        "currency": currency,
        "method": method,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }


def can_refund_payment(payment: dict, days_elapsed: int) -> bool:
    """Check if a completed payment is eligible for refund."""
    if not payment:
        return False
    if payment.get("status") != "completed":
        return False
    if days_elapsed < 0:
        return False
    return days_elapsed <= MAX_REFUND_DAYS


def calculate_partial_refund(original_amount: float, refund_percent: float) -> float:
    """Calculate partial refund amount."""
    if original_amount <= 0:
        raise ValueError("Original amount must be positive")
    if refund_percent < 0 or refund_percent > 100:
        raise ValueError("Refund percent must be 0-100")
    return round(original_amount * refund_percent / 100, 2)


def split_payment(total: float, num_installments: int) -> List[float]:
    """Split payment into equal installments, adjusting last for rounding."""
    if total <= 0:
        raise ValueError("Total must be positive")
    if num_installments < 1:
        raise ValueError("Must have at least 1 installment")

    per_installment = round(total / num_installments, 2)
    installments = [per_installment] * num_installments
    diff = round(total - sum(installments), 2)
    installments[-1] = round(installments[-1] + diff, 2)
    return installments


def convert_currency(
    amount: float, from_currency: str, to_currency: str, rates: Dict[str, float]
) -> float:
    """Convert amount between currencies using rate table (base USD)."""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
        raise ValueError("Unsupported currency")

    if from_currency == to_currency:
        return round(amount, 2)

    usd_amount = amount / rates.get(from_currency, 1.0)
    converted = usd_amount * rates.get(to_currency, 1.0)
    return round(converted, 2)


def aggregate_payments_by_method(payments: List[dict]) -> Dict[str, float]:
    """Sum completed payment amounts grouped by method."""
    totals: Dict[str, float] = {}
    for payment in payments:
        if payment.get("status") != "completed":
            continue
        method = payment.get("method", "unknown")
        totals[method] = totals.get(method, 0.0) + payment.get("amount", 0.0)
    return {k: round(v, 2) for k, v in totals.items()}


def validate_card_number(card_number: str) -> bool:
    """Validate card number using Luhn algorithm."""
    if not card_number or not card_number.isdigit():
        return False

    digits = [int(d) for d in card_number]
    checksum = 0
    reverse = digits[::-1]
    for i, d in enumerate(reverse):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0
