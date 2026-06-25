"""ItemPage - open an item, pick random variants, add to cart."""
from __future__ import annotations

from pages.base_page import BasePage


class ItemPage(BasePage):
    _ADD_TO_CART_BTN = None   # TODO: smart locator
    _VARIANT_SELECTS = None   # TODO: size/color/qty selectors (may be absent)

    def open(self, url: str) -> None:
        # TODO
        raise NotImplementedError

    def select_random_variants(self) -> None:
        """If variant pickers exist, choose a random available value for each."""
        # TODO: detect dropdowns/buttons, choose randomly among *enabled* options
        raise NotImplementedError

    def add_to_cart(self) -> None:
        # TODO: click add-to-cart; handle interstitials; screenshot per item
        raise NotImplementedError
