"""price_parser - turn eBay price strings into floats."""
from __future__ import annotations

import re

_PRICE_RE = re.compile(
    r"(?:(?:US\s*)?\$|[A-Z]{3}\s+)\s*([\d,]+(?:\.\d+)?)"
)


def parse_price(raw: str) -> float:
    """Parse a price string to a float.

    Handles: "$24.99", "$1,299.00", "US $24.99", "ILS 11.87", "EUR 9.50".
    Price ranges like "$12.00 to $18.00" return the lower bound.
    Raises ValueError on an unparseable string.
    """
    if not raw or not raw.strip():
        raise ValueError("Cannot parse price from empty string")

    matches = _PRICE_RE.findall(raw.strip())
    if not matches:
        raise ValueError(f"Cannot parse price from {raw!r}")

    try:
        return float(matches[0].replace(",", ""))
    except ValueError as exc:
        raise ValueError(f"Cannot parse price from {raw!r}") from exc