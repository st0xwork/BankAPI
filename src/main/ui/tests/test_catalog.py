import pytest

from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.utils.constants import TestUsers


pytestmark = pytest.mark.ui


def test_count_catalog(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    assert steps.get_products_count() == 6


def test_sorted_by_name(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    steps.sort_items("az")
    names = steps.get_product_names()
    assert names == sorted(names)

    steps.sort_items("za")
    names = steps.get_product_names()
    assert names == sorted(names, reverse=True)


def test_sort_by_price(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    steps.sort_items("lohi")
    prices = steps.get_product_prices()
    assert prices == sorted(prices)

    steps.sort_items("hilo")
    prices = steps.get_product_prices()
    assert prices == sorted(prices, reverse=True)


def test_add_to_cart(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    steps.add_to_cart("Sauce Labs Bike Light")

    assert steps.get_cart_count() == 1


def test_add_and_remove_onesie(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    steps.add_to_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 1

    steps.remove_from_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 0


def test_product_details_onesie(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    name, price, detail_name, detail_price = steps.open_product_details(
        "Sauce Labs Onesie"
    )

    assert name == detail_name
    assert price == detail_price


def test_product_details_fleece_jacket(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    name, price, detail_name, detail_price = steps.open_product_details(
        "Sauce Labs Fleece Jacket"
    )

    assert name == detail_name
    assert price == detail_price


def test_remove_item_from_catalog(page):
    steps = CatalogSteps(page)
    steps.login(TestUsers.STANDARD, TestUsers.PASSWORD)

    product_name = "Test.allTheThings() T-Shirt (Red)"

    steps.add_to_cart(product_name)
    assert steps.get_cart_count() == 1

    steps.remove_from_cart(product_name)
    assert steps.get_cart_count() == 0
