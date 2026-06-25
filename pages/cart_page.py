"""CartPage - open cart and read the total."""
from __future__ import annotations

from pages.base_page import BasePage


class CartPage(BasePage):
    _SUBTOTAL = None   # TODO: smart locator for subtotal/total text

    def open(self) -> None:
        # TODO: navigate to cart
        raise NotImplementedError

    def get_cart_total(self) -> float:
        """Read the subtotal/total as shown and return a float."""
        # TODO: read text, reuse utils.price_parser
        raise NotImplementedError
