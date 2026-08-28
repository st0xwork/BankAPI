from playwright.sync_api import Page
from src.main.ui.pages.base_page import BasePage


class BasketPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_link = page.locator(".shopping_cart_link")
        self.item_cards = page.locator(".cart_item")
        self.checkout_button = page.locator('[data-test="checkout"]')

    def open_cart(self):
        self.cart_link.click()

    def checkout(self):
        self.checkout_button.click()

    def remove_item(self, product_name: str):
        card = self.item_cards.filter(has_text=product_name)
        card.locator("button").click()

    def get_item_names(self) -> list[str]:
        return self.item_cards.locator(".inventory_item_name").all_text_contents()

    def get_item_prices(self) -> list[float]:
        prices = self.item_cards.locator(".inventory_item_price").all_text_contents()
        return [float(price.replace("$", "")) for price in prices]

    def get_item_total_price(self) -> float:
        return sum(self.get_item_prices())
