from locators import CartPageLocators as cart_locators
import allure

class CartPage:
    def __init__(self, page):
        self.page = page

    @allure.step("Get cart badge")
    def cart_badge(self):
        return self.page.locator(cart_locators.CART_BADGE)

    @allure.step("Open cart page")
    def open_cart(self):
        self.page.click(cart_locators.CART_LINK)

    @allure.step("Get cart items")
    def cart_items(self):
        return self.page.locator(cart_locators.CART_ITEM)

    @allure.step("Remove Sauce Labs Backpack from cart")
    def remove_backpack(self):
        self.page.click(cart_locators.REMOVE_BACKPACK_BUTTON)