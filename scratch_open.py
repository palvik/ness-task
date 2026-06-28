from playwright.sync_api import sync_playwright
from pages.search_page import SearchPage

print(">>> script started")

with sync_playwright() as pw:
    print(">>> launching browser")
    browser = pw.chromium.launch(headless=False, slow_mo=300)
    context = browser.new_context(base_url="https://www.ebay.com")
    page = context.new_page()
    print(">>> browser open, calling search_items_by_name_under_price()")

    sp = SearchPage(page)
    urls = sp.search_items_by_name_under_price("shoes", max_price=50, limit=5)

    print(f"got {len(urls)} urls:")
    for u in urls:
        print(" ", u)

    page.wait_for_timeout(4000)
    browser.close()

print(">>> done")