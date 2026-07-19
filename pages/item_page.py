"""ItemPage - open an item, pick random variants, add to cart."""
from __future__ import annotations

import random
import re

from playwright.sync_api import expect
from pages.base_page import BasePage

_ITEM_ID_RE = re.compile(r"/itm/(\d+)")


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

            # Exclude out-of-stock/disabled options (aria-disabled="true") -
            # picking one at random causes an unrecoverable timeout, since a
            # disabled option never becomes clickable no matter how long we wait.
            options = self.page.locator(
                f"#{listbox_id} [data-sku-value-name]:not([aria-disabled='true'])"
            )
            option_count = options.count()
            if option_count == 0:
                self.log.warning(
                    "no available (non-disabled) options in listbox %s, skipping",
                    listbox_id,
                )
                self.page.keyboard.press("Escape")
                continue

            chosen = options.nth(random.randint(0, option_count - 1))
            value_name = chosen.get_attribute("data-sku-value-name")
            chosen.click()

            listbox = self.page.locator(f"#{listbox_id}")
            try:
                expect(listbox).to_be_hidden(timeout=3000)
            except AssertionError:
                # some single-option listboxes don't auto-close; force it
                self.page.keyboard.press("Escape")

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

        dialog = self.page.get_by_role("dialog")

        # eBay shows a transitional "Still adding…" state after variant
        # selection (extra AJAX round-trip); asserting the final state too
        # early races that transition and produces an intermittent failure.
        still_adding = dialog.get_by_text("Still adding")
        if still_adding.is_visible():
            expect(still_adding).to_be_hidden(timeout=15000)

        # Main confirmation check
        added_text = self.page.get_by_text("Added to cart")
        go_to_cart_btn = self.page.get_by_role("button", name="Go to cart")

        # Fallback: confirmation text can differ across item templates,
        # but the "Go to cart" button appears reliably in both cases
        expect(added_text.or_(go_to_cart_btn)).to_be_visible(timeout=15000)

        match = _ITEM_ID_RE.search(self.page.url)
        item_id = match.group(1) if match else "unknown"
        self.screenshot(f"item_added_{item_id}")
        self.log.info("added item %s to cart", item_id)