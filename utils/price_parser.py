"""price_parser - turn eBay price strings into floats.

GRADED (part of the 35%): implement this yourself. Below is the contract and
the cases your unit tests should cover. Decide and DOCUMENT how you treat
ranges ("$12.00 to $18.00") - lower vs upper bound - in the README.
"""
from __future__ import annotations

import re

# Dollar ($, US $) or ISO currency code (EUR, ILS, …) followed by the amount.
_PRICE_RE = re.compile(
    r"(?:(?:US\s*)?\$|[A-Z]{3}\s+)\s*([\d,]+(?:\.\d+)?)",
)


def parse_price(raw: str) -> float:
    """Parse a price string to a float.

    Must handle at least:
      "$24.99"            -> 24.99
      "$1,299.00"         -> 1299.0     (thousands separator)
      "$12.00 to $18.00"  -> documented choice (lower or upper bound)
      "US $24.99"         -> 24.99
      "ILS 11.87"         -> 11.87
      "EUR 9.50"          -> 9.50
      stray whitespace / currency symbols

    Raise ValueError on an unparseable string rather than returning a wrong 0.0.

    Price ranges (e.g. "$12.00 to $18.00") return the lower bound — the "from"
    price eBay shows on multi-variant listings.
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
