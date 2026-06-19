# ShopCore

Python e-commerce backend utilities for orders, payments, inventory, and customer management.

## Setup

```bash
pip install -r requirements.txt
pytest
```

## Modules

| Module | Description |
|---|---|
| `order_service.py` | Orders, tax, pagination, refunds, status transitions |
| `user_auth.py` | Auth, sessions, roles, password hashing |
| `inventory.py` | Stock, warehouses, expiry, turnover |
| `cart_service.py` | Cart operations, coupons |
| `payment_service.py` | Payments, refunds, currency |
| `shipping_service.py` | Shipping rates, zones, weight |
| `pricing_engine.py` | Bulk/tier/dynamic pricing |
| `notification_service.py` | Email/SMS notifications |
| `db_queries.py` | Database query helpers |
