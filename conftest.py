"""Pytest fixtures: browser/context lifecycle, tracing, screenshots, Allure.

This is plumbing shared by all tests. The Browser -> Context -> Page hierarchy
mirrors Playwright's model; the trace is recorded at the *context* level and
saved per test, so every run leaves a trace.zip + failure screenshot.
"""
from __future__ import annotations

import os
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from core.config import CONFIG

REPORTS = Path(__file__).resolve().parent / "reports"
TRACES = REPORTS / "traces"
SHOTS = REPORTS / "screenshots"
for _d in (TRACES, SHOTS):
    _d.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def _playwright():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(_playwright) -> Browser:
    launcher = getattr(_playwright, CONFIG.browser_name)
    browser = launcher.launch(headless=CONFIG.headless, slow_mo=CONFIG.slow_mo_ms)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, request) -> BrowserContext:
    ctx = browser.new_context(...)
    ctx.set_default_timeout(CONFIG.default_timeout_ms)
    ctx.set_default_navigation_timeout(CONFIG.navigation_timeout_ms)
    if CONFIG.trace:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    if CONFIG.trace:
        trace_path = TRACES / f"{request.node.name}.zip"
        ctx.tracing.stop(path=str(trace_path))
        # прикладываем trace в Allure только если тест упал
        test_failed = (
            hasattr(request.node, "rep_call") and request.node.rep_call.failed
        )
        if trace_path.exists():
            if test_failed:
                allure.attach.file(str(trace_path), name="trace", extension="zip")
            else:
                trace_path.unlink()  # успешный прогон — trace не нужен, удаляем
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    return context.new_page()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to Allure when a test fails."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            shot = SHOTS / f"FAIL_{item.name}.png"
            try:
                page.screenshot(path=str(shot), full_page=True)
                allure.attach.file(
                    str(shot),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass  # never let teardown reporting crash the run
