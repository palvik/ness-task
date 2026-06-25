"""End-to-end scenario (the 4 functions wired together).

GRADED: assemble the flow using your page objects. Read inputs from
data/test_data.yaml (data-driven). Assert the cart total does not exceed
budget_per_item * items_count.
"""
from pathlib import Path

import allure
import pytest
import yaml

from pages.search_page import SearchPage
from pages.item_page import ItemPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage

DATA = Path(__file__).resolve().parent.parent / "data" / "test_data.yaml"
SCENARIOS = yaml.safe_load(DATA.read_text(encoding="utf-8"))["scenarios"]


def _ids(s):
    return s["name"]


@pytest.mark.e2e
@pytest.mark.parametrize("scenario", SCENARIOS, ids=_ids)
def test_cart_total_within_budget(page, scenario):
    query = scenario["query"]
    max_price = scenario["max_price"]
    limit = scenario["limit"]
    budget = scenario["budget_per_item"]

    # TODO: wire the flow:
    #   LoginPage(page).login_as_guest()
    #   urls = SearchPage(page).search_items_by_name_under_price(query, max_price, limit)
    #   ItemPage(page) -> add each url to cart (addItemsToCart)
    #   total = CartPage(page).get_cart_total()
    #   assert total <= budget * len(urls)   (assertCartTotalNotExceeds)
    raise NotImplementedError
