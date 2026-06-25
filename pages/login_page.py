"""LoginPage - per task email, CAPTCHA is out of scope.

Default strategy is guest browsing; a stub mode is allowed (document in README).
"""
from __future__ import annotations

from pages.base_page import BasePage


class LoginPage(BasePage):
    def login_as_guest(self) -> None:
        """No-op / ensure a clean guest session. Document the assumption."""
        # TODO: confirm we are browsing as guest (no auth needed for the flow).
        raise NotImplementedError

    def login_stub(self, username: str, password: str) -> None:
        """Optional stubbed login if you choose to demonstrate it."""
        # TODO: implement only if you go the stub route; avoid CAPTCHA.
        raise NotImplementedError
