from locators import ProductPageLocators as pd_locators
from locators import ProductDetailPageLocators as pdd_locators
import allure


class ProductPage:
    def __init__(self, page):
        self.page = page

    @allure.step("Get inventory container")
    def inventory_container(self):
        return self.page.locator(pd_locators.INVENTORY_CONTAINER)

    @allure.step("Get page title")
    def page_title(self):
        return self.page.locator(pd_locators.PAGE_TITLE)

    @allure.step("Get product items")
    def product_items(self):
        return self.page.locator(pd_locators.INVENTORY_ITEM)

    @allure.step("Open Sauce Labs Backpack detail")
    def open_backpack_detail(self):
        self.page.click(pd_locators.BACKPACK_LINK)

    @allure.step("Get detail product name")
    def detail_product_name(self):
        return self.page.locator(pdd_locators.ITEM_NAME)

    @allure.step("Get detail product description")
    def detail_product_description(self):
        return self.page.locator(pdd_locators.ITEM_DESC)
    
    @allure.step("Add Sauce Labs Backpack to cart")
    def add_backpack_to_cart(self):
        self.page.click(pd_locators.ADD_BACKPACK_BUTTON)