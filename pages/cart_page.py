"""CartPage - open cart and read the total."""
from __future__ import annotations

from pages.base_page import BasePage
from utils.price_parser import parse_price


class CartPage(BasePage):
    _CART_SUBTOTAL = "[data-test-id='SUBTOTAL']"

    def open(self) -> None:
        """Navigate to cart."""
        self.goto("https://cart.ebay.com")

    def get_cart_total(self) -> float:
        """Read the subtotal/total as shown and return a float."""
        subtotal_text = self.page.locator(self._CART_SUBTOTAL).inner_text()
        return parse_price(subtotal_text)
