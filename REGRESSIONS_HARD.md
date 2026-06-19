# Hard Test Case Ground Truth (`test2-hard` branch)

Score your bot against this checklist. **25 planted issues** — no `# BUG` comments in code.
Issues are mixed with legitimate-looking refactors across ~1760 lines and 9 modules.

## Difficulty tiers

| Tier | Count | Description |
|---|---|---|
| Obvious (test-breaking) | 18 | Caught by existing pytest suite |
| Subtle (no test coverage) | 7 | Requires static/diff analysis |

---

## `src/order_service.py` (9 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 1 | ~50 | bug | `apply_tax()` adds flat `tax_rate` to subtotal instead of applying percentage |
| 2 | ~61 | regression | `paginate()` uses `page * page_size` instead of `(page - 1) * page_size` |
| 3 | ~83 | regression | `is_order_eligible_for_refund()` uses `< 30` instead of `<= 30` |
| 4 | ~158 | regression | `filter_orders_by_date_range()` uses `< end` instead of `<= end` |
| 5 | ~170 | regression | `calculate_loyalty_points()` truncates with `int(order_total)` before multiplying tier |
| 6 | ~194 | regression | `estimate_delivery_date()` advances date before weekday check, skewing business-day count |
| 7 | ~181 | regression | `merge_order_items()` overwrites `price` from incoming item on SKU merge |
| 8 | ~16 | bug | `calculate_total()` removed negative price validation |
| 9 | ~27 | bug | `apply_discount()` removed 100% cap and `max(..., 0)` floor |

## `src/user_auth.py` (5 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 10 | ~26 | regression | `hash_password()` reversed to `password+salt` — invalidates existing hashes |
| 11 | ~34 | bug | `check_password()` uses `==` instead of `hmac.compare_digest()` — timing attack |
| 12 | ~52 | regression | `validate_password_strength()` accepts 6-char passwords (was 8) |
| 13 | ~93 | regression | `is_session_valid()` inverted — returns `True` when expired |
| 14 | ~39 | bug | `sanitize_username()` removed `None` guard — `AttributeError` on `None` |

## `src/inventory.py` (5 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 15 | ~13 | regression | `get_low_stock_items()` changed `<` to `<=` threshold |
| 16 | ~24 | bug | `reserve_stock()` removed insufficient-stock check |
| 17 | ~38 | regression | `calculate_reorder_quantity()` removed safety stock buffer |
| 18 | ~98 | regression | `get_expiring_items()` uses `< cutoff` — excludes items expiring on cutoff day |
| 19 | ~163 | regression | `calculate_turnover_rate()` uses `period_days/365` instead of `365/period_days` |
| 20 | ~66 | bug | `batch_reserve_stock()` rollback adds `reserved_qty` instead of restoring snapshot |

## `src/cart_service.py` (3 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 21 | ~68 | regression | `apply_coupon()` percent type subtracts `value/100` flat instead of percentage |
| 22 | ~84 | regression | `validate_coupon()` rejects orders above `min_order` (inverted comparison) |
| 23 | ~52 | bug | `get_cart_total()` sums prices only, ignores `quantity` |

## `src/payment_service.py` (3 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 24 | ~63 | regression | `can_refund_payment()` uses `< 90` instead of `<= 90` days |
| 25 | ~82 | bug | `split_payment()` uses `int()` truncation — loses cents, sum != total |
| 26 | ~128 | bug | `validate_card_number()` Luhn fix uses `d - 8` instead of `d - 9` |

## `src/shipping_service.py` (3 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 27 | ~54 | regression | Free shipping uses `>` threshold instead of `>=` — $75 orders pay shipping |
| 28 | ~74 | regression | Express delivery uses `days - 1` instead of `days // 2` |
| 29 | ~99 | bug | `get_billable_weight()` returns `min()` instead of `max()` |

## `src/pricing_engine.py` (3 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 30 | ~19 | regression | `get_bulk_discount()` uses `>` instead of `>=` — misses tier boundaries |
| 31 | ~68 | regression | `calculate_dynamic_price()` floor changed from 0.5 to 0.8 |
| 32 | ~79 | bug | `match_competitor_price()` returns competitor price without floor/max guard |

## `src/notification_service.py` (2 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 33 | ~47 | bug | `truncate_sms()` slices to `max_length` not `max_length - 3` — exceeds limit |
| 34 | ~72 | regression | `should_send_notification()` inverted muted check — sends muted, blocks others |

## `src/db_queries.py` (2 issues)

| # | Line | Type | Issue |
|---|---|---|---|
| 35 | ~9 | bug | `search_users_by_name()` SQL injection via f-string |
| 36 | ~26 | bug | `get_orders_by_user()` SQL injection via f-string interpolation |

---

## Test results

```
18 failed, 65 passed
```

## Scoring

```
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
```

Total ground truth issues: **36** (use table above).

## Create PR

```bash
gh pr create --base main --head test2-hard \
  --title "Refactor services and optimize query layer" \
  --body "Consolidates pricing logic, improves session handling, and adds optimized DB queries."
```
