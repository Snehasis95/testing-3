# testing-3

Test repository for regression and bug detection bot.

A Python e-commerce service (~1500+ lines) used to validate PR analysis accuracy.

## Setup

```bash
pip install -r requirements.txt
pytest
```

## Structure

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
| `db_queries.py` | Parameterized database queries |

## Test branches

| Branch | Difficulty | Issues |
|---|---|---|
| `test1` | Easy | 10 obvious bugs (original small codebase) |
| `test2-hard` | Hard | 25+ subtle regressions in expanded codebase |
