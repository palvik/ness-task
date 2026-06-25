"""Configuration loader: merges config/config.yaml with .env overrides.

Data-Driven principle: nothing about *where* we run is hardcoded in tests or
pages. Tests read settings from here; inputs (queries/prices) live in data/.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")  # silently no-ops if .env is absent


def _load_yaml() -> dict[str, Any]:
    with open(ROOT / "config" / "config.yaml", "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _as_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Config:
    base_url: str
    search_path: str
    browser_name: str
    headless: bool
    slow_mo_ms: int
    viewport: dict[str, int]
    default_timeout_ms: int
    navigation_timeout_ms: int
    currency: str
    locale: str
    trace: bool
    screenshots: bool
    login_mode: str
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @property
    def search_url(self) -> str:
        return f"{self.base_url}{self.search_path}"


def load_config() -> Config:
    y = _load_yaml()
    b = y["browser"]
    t = y["timeouts"]
    a = y["artifacts"]
    return Config(
        base_url=os.getenv("BASE_URL", y["base_url"]),
        search_path=y["search_path"],
        browser_name=os.getenv("BROWSER", b["name"]),
        headless=_as_bool(os.getenv("HEADLESS"), b["headless"]),
        slow_mo_ms=int(os.getenv("SLOW_MO_MS", b["slow_mo_ms"])),
        viewport=b["viewport"],
        default_timeout_ms=t["default_ms"],
        navigation_timeout_ms=t["navigation_ms"],
        currency=y["currency"],
        locale=y["locale"],
        trace=_as_bool(os.getenv("TRACE"), a["trace"]),
        screenshots=_as_bool(os.getenv("SCREENSHOTS"), a["screenshots"]),
        login_mode=os.getenv("LOGIN_MODE", "guest"),
        raw=y,
    )


CONFIG = load_config()
