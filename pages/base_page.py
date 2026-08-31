"""BasePage: thin parent for all page objects (SRP-friendly).

Holds the Playwright `page`, the logger, and a couple of generic helpers that
every page legitimately shares (navigation, screenshot). Page-specific logic
lives in the subclasses - keep this class small on purpose.
"""
from __future__ import annotations
from pathlib import Path
import allure
from playwright.sync_api import Page
from utils.logger import get_logger
import pytest

SHOTS = Path(__file__).resolve().parent.parent / "reports" / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)

BLOCK_MARKERS = (
    "Something went wrong on our end",   # eBay soft-block for datacenter IPs
    "Please verify yourself to continue",  # hCaptcha gate
)

class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.log = get_logger(self.__class__.__name__)

    def goto(self, url: str) -> None:
        self.log.info("navigate -> %s", url)
        self.page.goto(url, wait_until="domcontentloaded")
        self._bail_if_blocked(f"navigation to {url}")

    def screenshot(self, name: str) -> Path:
        """Save a full-page screenshot and attach it to the Allure report."""
        path = SHOTS / f"{name}.png"
        self.page.screenshot(path=str(path), full_page=True)
        allure.attach.file(
            str(path), name=name, attachment_type=allure.attachment_type.PNG
        )
        return path

    def _dismiss_consent_if_present(self) -> None:
        """Close cookie/consent banner if it appears. No-op if absent."""
        banner = self.page.get_by_role("button", name="Accept all")
        try:
            if banner.is_visible(timeout=2000):
                banner.click()
        except Exception:
            pass  # banner is not present - this is normal

    def _bail_if_blocked(self, context: str) -> None:
        """eBay serves an error/challenge page to CI IPs. Report as skip, not fail."""
        if "splashui/challenge" in self.page.url:
            marker = "splashui/challenge"
        else:
            body = self.page.locator("body").inner_text(timeout=5000)
            marker = next((m for m in BLOCK_MARKERS if m in body), None)
        if marker:
            self.screenshot("blocked_by_ebay")
            pytest.skip(f"eBay anti-bot page during {context} ({marker}) - not a test defect")