import pytest

from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps
from src.main.utils.constants import TestUsers, Urls


pytestmark = pytest.mark.ui


def test_login_valid_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login(TestUsers.STANDARD, TestUsers.PASSWORD)

    assert catalog.get_products_count() > 0, (
        "Ожидаем товары на странице каталога"
    )


def test_login_locked_out_user(page):
    login = LoginSteps(page)

    login.open_login_page().login(TestUsers.LOCKED_OUT, TestUsers.PASSWORD)

    error_text = login.get_error_text()

    assert "locked out" in error_text, (
        "Ожидаем сообщение о заблокированном пользователе"
    )


def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login(TestUsers.STANDARD, TestUsers.PASSWORD)

    assert catalog.get_products_count() > 0, (
        "Ожидаем, что в каталоге есть товары"
    )

    catalog.logout()

    assert page.url == f"{Urls.BASE}/", (
        "Ожидаем возврат на страницу логина"
    )


def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login(TestUsers.VISUAL, TestUsers.PASSWORD)

    assert catalog.get_products_count() > 0, (
        "Ожидаем, что в каталоге есть товары"
    )

    catalog.logout()

    assert page.url == f"{Urls.BASE}/", (
        "Ожидаем возврат на страницу логина"
    )
