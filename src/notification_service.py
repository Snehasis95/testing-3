"""Notification service for customer communications."""

from datetime import datetime
from typing import Dict, List, Optional

MAX_SMS_LENGTH = 160
VALID_CHANNELS = {"email", "sms", "push"}


def build_order_confirmation_email(order: dict, user: dict) -> dict:
    """Build order confirmation email payload."""
    if not order or not user:
        raise ValueError("Order and user are required")

    return {
        "to": user.get("email"),
        "subject": f"Order Confirmation #{order.get('id', 'N/A')}",
        "body": (
            f"Hi {user.get('first_name', 'Customer')},\n\n"
            f"Your order #{order.get('id')} has been confirmed.\n"
            f"Total: ${order.get('total', 0):.2f}\n\n"
            f"Thank you for shopping with us!"
        ),
        "channel": "email",
        "created_at": datetime.utcnow().isoformat(),
    }


def build_shipping_notification(order: dict, tracking_number: str) -> dict:
    """Build shipping notification payload."""
    return {
        "subject": f"Your order #{order.get('id')} has shipped!",
        "body": f"Track your package: {tracking_number}",
        "channel": "email",
        "metadata": {"tracking_number": tracking_number},
    }


def truncate_sms(message: str, max_length: int = MAX_SMS_LENGTH) -> str:
    """Truncate SMS message to max length."""
    if not message:
        return ""
    if max_length < 1:
        raise ValueError("max_length must be at least 1")
    if len(message) <= max_length:
        return message
    return message[: max_length - 3] + "..."


def validate_notification_preferences(prefs: dict) -> bool:
    """Validate user notification preferences structure."""
    if not prefs:
        return False
    for channel in prefs:
        if channel not in VALID_CHANNELS:
            return False
        if not isinstance(prefs[channel], bool):
            return False
    return True


def should_send_notification(prefs: dict, channel: str, notification_type: str) -> bool:
    """Determine if notification should be sent based on preferences."""
    if channel not in VALID_CHANNELS:
        return False
    if not prefs:
        return True
    if not prefs.get(channel, True):
        return False

    muted = prefs.get("muted_types", [])
    return notification_type not in muted


def batch_notifications(notifications: List[dict], batch_size: int = 50) -> List[List[dict]]:
    """Split notifications into batches for processing."""
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")
    return [notifications[i : i + batch_size] for i in range(0, len(notifications), batch_size)]


def format_currency_in_message(amount: float, currency: str = "USD") -> str:
    """Format currency for notification messages."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:.2f}"


def build_refund_notification(order_id: str, refund_amount: float) -> dict:
    """Build refund notification."""
    return {
        "subject": f"Refund processed for order #{order_id}",
        "body": f"A refund of {format_currency_in_message(refund_amount)} has been processed.",
        "channel": "email",
        "type": "refund",
    }


def deduplicate_notifications(notifications: List[dict]) -> List[dict]:
    """Remove duplicate notifications by subject and recipient."""
    seen = set()
    unique = []
    for notif in notifications:
        key = (notif.get("to"), notif.get("subject"))
        if key not in seen:
            seen.add(key)
            unique.append(notif)
    return unique


def get_notification_priority(notification_type: str) -> int:
    """Return priority level (1=highest, 3=lowest)."""
    priorities = {
        "security_alert": 1,
        "order_confirmation": 2,
        "shipping_update": 2,
        "promotional": 3,
        "newsletter": 3,
    }
    return priorities.get(notification_type, 2)
