"""LoginPage - per task email, CAPTCHA is out of scope.

Default strategy is guest browsing; a stub mode is allowed (document in README).
"""
from __future__ import annotations
from playwright.sync_api import expect
from core.config import CONFIG
from pages.base_page import BasePage

class LoginPage(BasePage):
    def login_as_guest(self) -> None:
        """No-op / ensure a clean guest session. Document the assumption."""
        self.goto(CONFIG.base_url)
        self._dismiss_consent_if_present()
        expect(self.page.get_by_role("link", name="Sign in")).to_be_visible()
        self.log.info("confirmed guest session (no sign-in detected)")

    def login_stub(self, username: str, password: str) -> None:
        """Optional stubbed login if you choose to demonstrate it."""
        # TODO: implement only if you go the stub route; avoid CAPTCHA.
        raise NotImplementedError