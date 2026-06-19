# testing-3

Test repository for regression and bug detection bot.

A small Python order/inventory service used to validate PR analysis accuracy.

## Setup

```bash
pip install -r requirements.txt
pytest
```

## Structure

- `src/order_service.py` — order totals, discounts, pagination, refunds
- `src/user_auth.py` — email validation, password hashing
- `src/inventory.py` — stock management and reorder logic
