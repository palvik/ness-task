"""LoginPage - guest session only.

CAPTCHA handling is out of scope for this project; the flow simply
confirms a clean guest session before proceeding.
"""
from __future__ import annotations
from playwright.sync_api import expect
from core.config import CONFIG
from pages.base_page import BasePage


class LoginPage(BasePage):
    def login_as_guest(self) -> None:
        """Confirm a clean guest session (no authentication performed)."""
        self.goto(CONFIG.base_url)
        self._dismiss_consent_if_present()
        expect(self.page.get_by_role("link", name="Sign in")).to_be_visible()
        self.log.info("confirmed guest session (no sign-in detected)")