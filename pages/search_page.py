"""SearchPage - search + price filter + pagination + URL collection.

This is the core of the 35% (robustness & smart locators). Implement the
method bodies yourself and verify every locator against live eBay
(playwright codegen / DevTools). XPath is required for result extraction
per the task; prefer get_by_role/label for the filter inputs and Next button.
"""
from __future__ import annotations
from pages.base_page import BasePage
from core.config import CONFIG
from utils.price_parser import parse_price
import re
from playwright.sync_api import expect


class SearchPage(BasePage):
    # --- LOCATORS: verify on the live site; eBay class names rotate ---
    _ITEM_ID_RE = re.compile(r"/itm/(\d{9,})")
    _RESULTS_ITEMS = "xpath=//li[contains(@class,'s-card')]" 
    _ITEM_LINK = "xpath=.//a[contains(@href,'/itm/')]"
    _ITEM_PRICE = "xpath=.//span[contains(@class,'s-card__price')]"
    _PRICE_MAX_INPUT = "xpath=.//input[contains(@name,'maxPrice')]"
    _APPLY_PRICE_BTN = None               # TODO
    _NEXT_BUTTON = None                   # TODO: e.g. get_by_role("button", name="Next")
    _SEARCH_INPUT_NAME = "Search for anything"
    _SEARCH_BUTTON_NAME = "Search"

    def open(self, query: str) -> None:
        """Open the results page for `query`."""
        self.goto(CONFIG.base_url)
        self._dismiss_consent_if_present()
        self.page.get_by_role("combobox", name=self._SEARCH_INPUT_NAME).fill(query)
        self.page.get_by_role("button", name=self._SEARCH_BUTTON_NAME, exact=True).click()
        expect(self.page).to_have_url(re.compile(r"/sch/"))
        expect(self.page.locator(self._RESULTS_ITEMS).first).to_be_visible()
        self.log.info("search opened for query=%r", query)        


    def apply_max_price(self, max_price: float) -> None:
        """Use the page's min/max price filter to cap at max_price."""
        # TODO: fill max field, apply, wait for the list to re-render (expect, not sleep)
        raise NotImplementedError

    def _parse_current_page(self, max_price: float) -> list[str]:
        """Return cleaned hrefs on the current page with price <= max_price."""
        hrefs: list[str] = []
        for card in self.page.locator(self._RESULTS_ITEMS).all():
            try:
                price_text = " ".join(card.locator(self._ITEM_PRICE).all_inner_texts())
                price = parse_price(price_text)
                if price <= max_price:
                    href = card.locator(self._ITEM_LINK).first.get_attribute("href")
                    if href:
                        clean_href = href.split("?")[0]
                        if self._ITEM_ID_RE.search(clean_href):
                            hrefs.append(clean_href)        
            except ValueError:
                continue
        return hrefs

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
