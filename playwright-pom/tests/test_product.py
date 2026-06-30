import allure
from playwright.sync_api import expect

@allure.feature("Product Feature")
@allure.link("https://www.saucedemo.com/inventory.html", name="Product Page")
class TestProduct:

    @allure.story("Display product list")
    @allure.title("TC_PRODUCT_001: Hiển thị danh sách sản phẩm")
    def test_display_product_list(self, open_product_page):
        expect(open_product_page.inventory_container()).to_be_visible()
        expect(open_product_page.page_title()).to_have_text("Products")
        expect(open_product_page.product_items()).to_have_count(6)

    @allure.story("View product detail")
    @allure.title("TC_PRODUCT_002: Xem chi tiết sản phẩm")
    def test_view_product_detail(self, open_product_page):
        open_product_page.open_backpack_detail()
        expect(open_product_page.page).to_have_url(
            "https://www.saucedemo.com/inventory-item.html?id=4"
        )
        expect(open_product_page.detail_product_name()).to_have_text("Sauce Labs Backpack")
        expect(open_product_page.detail_product_description()).to_be_visible()