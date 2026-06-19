from src.notification_service import (
    batch_notifications,
    build_order_confirmation_email,
    deduplicate_notifications,
    get_notification_priority,
    should_send_notification,
    truncate_sms,
    validate_notification_preferences,
)


def test_build_order_confirmation_email():
    order = {"id": "123", "total": 99.99}
    user = {"email": "a@b.com", "first_name": "Alice"}
    email = build_order_confirmation_email(order, user)
    assert "123" in email["subject"]


def test_truncate_sms():
    long_msg = "x" * 200
    result = truncate_sms(long_msg)
    assert len(result) == 160


def test_validate_notification_preferences():
    prefs = {"email": True, "sms": False}
    assert validate_notification_preferences(prefs) is True


def test_should_send_notification():
    prefs = {"email": True, "muted_types": ["promotional"]}
    assert should_send_notification(prefs, "email", "order_confirmation") is True
    assert should_send_notification(prefs, "email", "promotional") is False


def test_batch_notifications():
    notifs = [{"id": i} for i in range(5)]
    batches = batch_notifications(notifs, batch_size=2)
    assert len(batches) == 3


def test_deduplicate_notifications():
    notifs = [
        {"to": "a@b.com", "subject": "Hi"},
        {"to": "a@b.com", "subject": "Hi"},
        {"to": "c@d.com", "subject": "Hi"},
    ]
    assert len(deduplicate_notifications(notifs)) == 2


def test_get_notification_priority():
    assert get_notification_priority("security_alert") == 1
    assert get_notification_priority("promotional") == 3
