"""End-to-end scenario (the 4 functions wired together).

GRADED: assemble the flow using your page objects. Read inputs from
data/test_data.yaml (data-driven). Assert the cart total does not exceed
budget_per_item * items_count.
"""
from pathlib import Path

import allure
import pytest
import yaml
import random

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

    with allure.step("Login as guest"):
        LoginPage(page).login_as_guest()
    
    with allure.step(f"Search '{query}' under price {max_price}"):
        urls = SearchPage(page).search_items_by_name_under_price(query, max_price, limit)

    if not urls:
        pytest.skip(f"No items found under {max_price} for query={query!r}")        

    with allure.step(f"Add {len(urls)} items to cart"):
        for url in urls:
            ItemPage(page).open(url)
            ItemPage(page).select_random_variants()
            ItemPage(page).add_to_cart()
            page.wait_for_timeout(random.randint(800, 2000))  # human-like pause to avoid Captcha
    
    with allure.step(f"Assert cart total not exceeds budget {budget * len(urls)}"):
        cart = CartPage(page)
        cart.open()
        total = cart.get_cart_total()
        assert total <= budget * len(urls)