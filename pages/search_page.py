"""SearchPage - search + price filter + pagination + URL collection.

This is the core of the 35% (robustness & smart locators). Implement the
method bodies yourself and verify every locator against live eBay
(playwright codegen / DevTools). XPath is required for result extraction
per the task; prefer get_by_role/label for the filter inputs and Next button.
"""
from __future__ import annotations

from pages.base_page import BasePage
from utils.price_parser import parse_price  # noqa: F401  (used once implemented)


class SearchPage(BasePage):
    # --- LOCATORS: verify on the live site; eBay class names rotate ---
    _RESULTS_ITEMS = "xpath=//..."        # TODO: result card containers
    _ITEM_LINK = "xpath=.//a[...]"        # TODO: /itm/ link inside a card
    _ITEM_PRICE = "xpath=.//span[...]"    # TODO: price text inside a card
    _PRICE_MAX_INPUT = None               # TODO: smart locator (role/label)
    _APPLY_PRICE_BTN = None               # TODO
    _NEXT_BUTTON = None                   # TODO: e.g. get_by_role("button", name="Next")

    def open(self, query: str) -> None:
        """Open the results page for `query`."""
        # TODO: goto search_url with _nkw=query, OR type into the search box + submit
        raise NotImplementedError

    def apply_max_price(self, max_price: float) -> None:
        """Use the page's min/max price filter to cap at max_price."""
        # TODO: fill max field, apply, wait for the list to re-render (expect, not sleep)
        raise NotImplementedError

    def _parse_current_page(self, max_price: float) -> list[str]:
        """Return cleaned hrefs on the current page with price <= max_price."""
        # TODO: iterate _RESULTS_ITEMS, parse_price(), filter, strip tracking query
        raise NotImplementedError

    def _go_to_next_page(self) -> bool:
        """Advance to the next page. Return True if it worked, else False."""
        # TODO: check Next is present/enabled, click, wait for new results
        raise NotImplementedError

    def search_items_by_name_under_price(
        self, query: str, max_price: float, limit: int = 5
    ) -> list[str]:
        """Up to `limit` item URLs priced <= max_price (see designed algorithm)."""
        # TODO: assemble open -> apply_max_price -> collect across pages -> [:limit]
        raise NotImplementedError
