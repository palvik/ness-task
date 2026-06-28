from playwright.sync_api import sync_playwright
from pages.search_page import SearchPage

print(">>> script started")

with sync_playwright() as pw:
    print(">>> launching browser")
    browser = pw.chromium.launch(headless=False, slow_mo=300)
    context = browser.new_context(base_url="https://www.ebay.com")
    page = context.new_page()
    print(">>> browser open, calling open()")

    sp = SearchPage(page)
    sp.open("shoes")
    sp.apply_max_price(50)
    print("URL after filter:", page.url)
    print("cards found after filter:", page.locator(SearchPage._RESULTS_ITEMS).count())

    urls = sp._parse_current_page(max_price=50)
    print(f"urls under 50: {len(urls)}")
    for u in urls[:5]:
        print(" ", u)
print(">>> done")