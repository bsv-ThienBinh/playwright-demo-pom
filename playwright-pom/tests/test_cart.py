import allure
from playwright.sync_api import expect
from pages.cart_page import CartPage


@allure.feature("Cart Feature")
@allure.link("https://www.saucedemo.com/cart.html", name="Cart Page")
class TestCart:

    @allure.story("Add product to cart")
    @allure.title("TC_CART_001: Add product vào cart")
    def test_add_product_to_cart(self, open_product_page):
        open_product_page.add_backpack_to_cart()
        cart_page = CartPage(open_product_page.page)
        expect(cart_page.cart_badge()).to_be_visible()
        expect(cart_page.cart_badge()).to_have_text("1")

    @allure.story("Remove product from cart")
    @allure.title("TC_CART_002: Remove product khỏi cart")
    def test_remove_product_from_cart(self, open_product_page):
        open_product_page.add_backpack_to_cart()
        cart_page = CartPage(open_product_page.page)
        cart_page.open_cart()
        expect(cart_page.page).to_have_url("https://www.saucedemo.com/cart.html")
        cart_page.remove_backpack()
        expect(cart_page.cart_items()).to_have_count(0)