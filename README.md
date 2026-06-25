# eBay E2E Automation - Playwright + Python (POM)

End-to-end scenario on eBay: search with a price condition, add items to cart,
and assert the cart total stays within budget. Built with Page Object Model,
OOP, and data-driven inputs.

## Prerequisites
- Python 3.11+
- Allure CLI (for the HTML report) - https://allurereport.org/docs/install/

## Setup
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
playwright install chromium

cp config/.env.example .env   # then edit if needed
```

## Run
```bash
pytest                      # runs e2e + unit, writes reports/allure-results
pytest -m unit              # just the price-parser unit tests
allure serve reports/allure-results          # interactive report
# or a self-contained file to commit:
allure generate reports/allure-results --single-file -o reports/html
```

## Architecture
- `pages/` - Page Objects (one page = one class, SRP). `search_page` holds the
  search/filter/pagination logic; `item_page` adds to cart; `cart_page` reads totals.
- `core/` - config loading (yaml + .env), browser factory concerns.
- `utils/` - reusable helpers: `price_parser` (unit-tested), logger.
- `data/` - data-driven scenarios (`test_data.yaml`).
- `tests/` - the wired e2e flow + unit tests.
- `conftest.py` - fixtures: context/page, tracing, screenshot-on-failure, Allure.

## The four functions
1. Login - guest (CAPTCHA out of scope per task brief).
2. `search_items_by_name_under_price(query, max_price, limit=5)` -> item URLs.
3. `add_items_to_cart(urls)` - random variant selection, screenshot per item.
4. `assert_cart_total_not_exceeds(budget_per_item, items_count)`.

## Assumptions & limitations  (TODO: fill in)
- **Login**: guest browsing; no authentication. CAPTCHA explicitly out of scope.
- **Currency**: USD on ebay.com.
- **Price ranges**: "$12 to $18" is treated as <lower|upper> bound -> EXPLAIN your choice.
- **Locators**: eBay rotates CSS class names; XPath used for result extraction
  per the task, semantic locators (role/label) for controls.

## Reports
Allure results in `reports/allure-results`; traces in `reports/traces`;
screenshots in `reports/screenshots`. CI (GitHub Actions) uploads all as artifacts.
