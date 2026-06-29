# AI-Generated Code Review - Static Analysis

> Task: review the AI-written test (static analysis, no tools), identify at
> least 3 problems, explain them, and propose fixes for the offending lines.

## Code under review
```python
from playwright.sync_api import sync_playwright
from selenium import webdriver
import time

def test_search_functionality():
    browser = sync_playwright().start().chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    time.sleep(2)

    search_box = page.locator("#search")
    search_box.fill("playwright testing")

    page.locator(".button").click()

    time.sleep(3)

    results = page.locator(".result-item")

    browser.close()
```

## Issues found

1. **Redundant import of Selenium WebDriver** — `from selenium import webdriver` is imported but never used. The entire test uses Playwright. This is dead code resulting from a copy-paste mistake or framework confusion. Fix: remove the import line entirely.

2. **`sync_playwright()` not used as a context manager** — Calling `sync_playwright().start()` without a `with` block means the underlying Playwright process is never properly stopped. Only the browser is closed, leaking the playwright instance. Fix:
   ```python
   with sync_playwright() as p:
       browser = p.chromium.launch()
   ```

3. **`time.sleep()` used instead of Playwright's built-in waiting** — Hard-coded sleeps (`time.sleep(2)`, `time.sleep(3)`) are an anti-pattern. They waste time when the page loads faster, and cause flakiness when it loads slower. Playwright has auto-waiting built into actions and explicit wait APIs. Fix:
   ```python
   page.wait_for_selector("#search")
   page.wait_for_load_state("networkidle")
   ```

4. **`results` locator is never asserted** — The locator `page.locator(".result-item")` is created and stored in `results`, but no assertion or interaction follows. The test will always pass even if zero results are returned, making it worthless as a test. Fix:
   ```python
   expect(results.first).to_be_visible()
   ```

5. **No error safety — `browser.close()` is skipped on exception** — If any line before `browser.close()` raises an exception, the browser stays open and resources leak. Fix: use a `with` block (which handles cleanup automatically) or a `try/finally` block.

6. **Overly generic selector `.button`** — The class `.button` can match multiple elements on the page. In Playwright strict mode this raises an error; even when it doesn't, clicking the wrong element silently breaks the test. Fix: use a specific role or test-id selector:
   ```python
   page.get_by_role("button", name="Search").click()
   ```
