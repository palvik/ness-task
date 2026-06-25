"""Unit tests for the price parser (fast, no browser).

GRADED: fill these in as you implement parse_price. Parametrize the cases.
"""
import pytest

from utils.price_parser import parse_price


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw, expected",
    [
        # ("$24.99", 24.99),
        # ("$1,299.00", 1299.0),
        # ("US $24.99", 24.99),
        # add range + edge cases here
    ],
)
def test_parse_price(raw, expected):
    assert parse_price(raw) == pytest.approx(expected)
