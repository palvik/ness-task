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

SHOTS = Path(__file__).resolve().parent.parent / "reports" / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.log = get_logger(self.__class__.__name__)

    def goto(self, url: str) -> None:
        self.log.info("navigate -> %s", url)
        self.page.goto(url, wait_until="domcontentloaded")

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
        banner = self.page.get_by_role("button", name="Accept all")  # TODO: check the text
        try:
            if banner.is_visible(timeout=2000):
                banner.click()
        except Exception:
            pass  # banner is not present - this is normal
