from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

print(">>> script started")

with sync_playwright() as pw:
    print(">>> launching browser")
    browser = pw.chromium.launch(headless=False, slow_mo=300)
    context = browser.new_context(base_url="https://www.ebay.com")
    page = context.new_page()
    print(">>> browser open, calling search_items_by_name_under_price()")

    lp = LoginPage(page)
    lp.login_as_guest()
    print("guest session confirmed")

    page.wait_for_timeout(4000)
    browser.close()

print(">>> done")