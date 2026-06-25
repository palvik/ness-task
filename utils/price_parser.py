"""price_parser - turn eBay price strings into floats.

GRADED (part of the 35%): implement this yourself. Below is the contract and
the cases your unit tests should cover. Decide and DOCUMENT how you treat
ranges ("$12.00 to $18.00") - lower vs upper bound - in the README.
"""
from __future__ import annotations


def parse_price(raw: str) -> float:
    """Parse a price string to a float.

    Must handle at least:
      "$24.99"            -> 24.99
      "$1,299.00"         -> 1299.0     (thousands separator)
      "$12.00 to $18.00"  -> documented choice (lower or upper bound)
      "US $24.99"         -> 24.99
      stray whitespace / currency symbols

    Raise ValueError on an unparseable string rather than returning a wrong 0.0.
    """
    # TODO: implement (regex or manual cleanup). Keep it pure + unit-tested.
    raise NotImplementedError
