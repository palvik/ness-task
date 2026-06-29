"""ItemPage - open an item, pick random variants, add to cart."""
from __future__ import annotations

import random
import re
from playwright.sync_api import expect
from pages.base_page import BasePage

class ItemPage(BasePage):
    def open(self, url: str) -> None:
        """Open the item page at `url`."""
        self.goto(url)

    def select_random_variants(self) -> None:
        """If variant pickers exist, choose a random available value for each."""
        variant_buttons = self.page.locator(
            "[data-testid='x-msku-evo'] button[aria-haspopup='listbox']"
        )
        count = variant_buttons.count()
        if count == 0:
            self.log.info("no variant selectors found, skipping")
            return

        for i in range(count):
            btn = variant_buttons.nth(i)
            listbox_id = btn.get_attribute("aria-controls")
            if not listbox_id:
                self.log.warning("variant button %d has no aria-controls, skipping", i)
                continue

            btn.click()

            options = self.page.locator(f"#{listbox_id} [data-sku-value-name]")
            option_count = options.count()
            if option_count == 0:
                self.log.warning("no options in listbox %s, skipping", listbox_id)
                continue

            chosen = options.nth(random.randint(0, option_count - 1))
            value_name = chosen.get_attribute("data-sku-value-name")
            chosen.click()
            self.log.info(
                "selected variant %d/%d: %r in listbox %s",
                i + 1,
                count,
                value_name,
                listbox_id,
            )

    def add_to_cart(self) -> None:
        """Click add-to-cart; handle interstitials; screenshot per item."""
        self.page.get_by_role("button", name="Add to cart").click()

        expect(self.page.get_by_text("Added to cart")).to_be_visible()

        item_id_match = re.search(r"/itm/(\d+)", self.page.url)
        item_id = item_id_match.group(1) if item_id_match else "unknown"
        self.screenshot(f"add_to_cart_{item_id}")

        self.page.get_by_role("button", name="Close dialog").click()
        self.log.info("added item %s to cart", item_id)