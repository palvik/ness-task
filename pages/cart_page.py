"""CartPage - open cart and read the total."""
from __future__ import annotations

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from utils.price_parser import parse_price


class CartPage(BasePage):
    _CART_SUBTOTAL = "[data-test-id='SUBTOTAL']"

    def open(self) -> None:
        """Navigate to cart."""
        self.goto("https://cart.ebay.com")

    def get_cart_total(self) -> float:
        # eBay occasionally serves an hCaptcha verification page instead of
        # the cart (anti-bot check, more likely under headless/datacenter
        # conditions). This is a known limitation of the target site, not a
        # bug in the locator - detect it early and fail with a clear reason
        # instead of a confusing "locator not found" timeout.
        captcha_notice = self.page.get_by_text("Please verify yourself to continue")
        if captcha_notice.is_visible(timeout=2000):
            self.screenshot("captcha_blocked")
            pytest.skip(
                "eBay anti-bot verification (hCaptcha) blocked this run - "
                "known limitation, see README"
            )

        try:
            subtotal_text = self.page.locator(self._CART_SUBTOTAL).inner_text(timeout=15000)
        except PlaywrightTimeoutError:
            # Locator not found within timeout - dump page state for diagnosis
            # instead of guessing at the selector blind
            self.page.screenshot(path="debug_cart_failure.png", full_page=True)
            with open("debug_cart_failure.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            self.log.error(
                "CART_SUBTOTAL locator not found; dumped screenshot and HTML "
                "to debug_cart_failure.png / debug_cart_failure.html"
            )
            raise

        return parse_price(subtotal_text)