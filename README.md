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
pytest -m unit              # just the price-parser unit tests (always reliable)
pytest -m e2e --headed      # e2e against live eBay (headed recommended locally)
allure serve reports/allure-results          # interactive report (requires Allure CLI)
# or a self-contained file to share:
allure generate reports/allure-results --single-file -o reports/html
# Windows helpers (auto-download Allure CLI to tools/allure on first run):
.\scripts\allure-serve.ps1
.\scripts\allure-generate.ps1
```

For local e2e runs, use headed mode to reduce bot-detection issues:

```bash
HEADLESS=false pytest -m e2e --headed
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
- **Currency**: eBay displays prices in the currency determined by the
  runner's geolocation (e.g. ILS when run from Israel, USD from the US).
  `parse_price()` is currency-agnostic — it extracts the numeric value
  regardless of symbol/code. `maxPrice`/`budgetPerItem` are compared in
  whatever currency the site returns; currency conversion is out of scope.
- **Price ranges**: "$12 to $18" uses the **lower** bound (the "from" price on
  multi-variant listings). Upper-bound parsing would exclude valid items when
  comparing against a max-price filter; the cart step uses the actual variant
  price, not the search-result range.
- **Locators**: eBay rotates CSS class names; XPath used for result extraction
  per the task, semantic locators (role/label) for controls.
- **Sponsored placeholders**: eBay injects "Shop on eBay" sponsored cards
  into search results with fake price/ID data (e.g. `/itm/123456`) to blend
  in with real listings. Filtered out by validating that the item ID in the
  href matches eBay's real ID format (9+ digits).  
- **CAPTCHA/anti-bot avoidance**: pagination advances by clicking the real
  "Next" link rather than jumping via URL params, to avoid triggering eBay's
  bot-detection (`splashui/challenge`) — confirmed experimentally that an
  aggressive jump (e.g. `_pgn=999`) triggers it. `_go_to_next_page()` is
  wrapped in try/except to gracefully stop pagination on any unexpected page
  state (including a potential challenge page) rather than crashing the run.  

## Reports

Every `pytest` run writes raw Allure data (JSON + attachments) to
`reports/allure-results/`. That folder is not browsable on its own — use the
[Allure CLI](https://allurereport.org/docs/install/) or the Windows scripts above
to render it.

**What is captured**

- Test steps from `allure.step` in the e2e test
- Playwright trace zips (attached per test from `conftest.py`)
- Failure screenshots and item screenshots

**Open the report**

| Goal | Command |
|------|---------|
| Interactive (recommended) | `allure serve reports/allure-results` or `.\scripts\allure-serve.ps1` |
| Static HTML file | `allure generate reports/allure-results --single-file -o reports/html` then open `reports/html/index.html` |
| CI artifacts | Download the `allure-results` artifact from GitHub Actions, extract, then `allure serve path/to/allure-results` |

**Related artifacts**

- Playwright traces: `reports/traces/*.zip` — `playwright show-trace reports/traces/<test_name>.zip`
- Screenshots: `reports/screenshots/`

CI (GitHub Actions) uploads `allure-results` and `playwright-artifacts` as workflow artifacts.
