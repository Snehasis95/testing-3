# Expected Regressions & Bugs (for manual bot accuracy scoring)

Use this checklist to score your bot against the `test1` branch.

## `src/order_service.py`

| # | Type | Issue | Expected detection |
|---|------|-------|-------------------|
| 1 | Regression | `paginate()` uses 0-indexed math (`page * page_size`) instead of 1-indexed | Off-by-one on page 1 returns wrong slice |
| 2 | Regression | `is_order_eligible_for_refund()` changed `<= 30` to `< 30` | Day-30 refunds incorrectly denied |
| 3 | Bug | `calculate_total()` no longer rejects negative prices | Invalid negative totals allowed |
| 4 | Bug | `apply_discount()` removed 100% cap and `max(..., 0)` floor | Discounts >100% produce negative totals |

## `src/user_auth.py`

| # | Type | Issue | Expected detection |
|---|------|-------|-------------------|
| 5 | Regression | `hash_password()` reversed salt/password concatenation order | All existing password hashes invalidated |
| 6 | Bug | `sanitize_username()` removed `None` guard | `AttributeError` when `username` is `None` |

## `src/inventory.py`

| # | Type | Issue | Expected detection |
|---|------|-------|-------------------|
| 7 | Regression | `get_low_stock_items()` changed `<` to `<=` | Items at exactly threshold wrongly flagged |
| 8 | Bug | `reserve_stock()` removed insufficient-stock check | Inventory can go negative |
| 9 | Regression | `calculate_reorder_quantity()` removed safety stock buffer | Under-ordering risk |

## `src/db_queries.py` (new file)

| # | Type | Issue | Expected detection |
|---|------|-------|-------------------|
| 10 | Bug | `search_users_by_name()` uses f-string SQL interpolation | SQL injection vulnerability |

## Failing tests

Running `pytest` on this branch produces **3 failures** against the unchanged test suite. Other bugs are not covered by existing tests.

```bash
pip install -r requirements.txt
pytest -v
```

## Create the PR

```bash
gh pr create --base main --head test1 \
  --title "Refactor order and inventory handling" \
  --body "Performance improvements and query helper additions."
```
