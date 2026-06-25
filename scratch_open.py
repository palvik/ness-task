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
    print(">>> open() returned")

    print("URL:", page.url)
    print("cards found:", page.locator(SearchPage._RESULTS_ITEMS).count())

    page.wait_for_timeout(4000)
    browser.close()

print(">>> done")