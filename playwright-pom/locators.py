class LoginPageLocators:
    INPUT_USERNAME = "#user-name"
    INPUT_PASSWORD = "#password" 
    BUTTON_LOGIN = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"


class ProductPageLocators:
    INVENTORY_CONTAINER = "[data-test='inventory-container']"
    PAGE_TITLE = ".title"
    INVENTORY_LIST = "[data-test='inventory-list']"
    INVENTORY_ITEM = "[data-test='inventory-item']"
    BACKPACK_LINK = "[data-test='item-4-title-link']"
    ADD_BACKPACK_BUTTON = "[data-test='add-to-cart-sauce-labs-backpack']"


class ProductDetailPageLocators:
    ITEM_NAME = "[data-test='inventory-item-name']"
    ITEM_DESC = "[data-test='inventory-item-desc']"
class CartPageLocators:
    CART_LINK = "[data-test='shopping-cart-link']"
    CART_BADGE = "[data-test='shopping-cart-badge']"
    CART_ITEM = "[data-test='inventory-item']"
    REMOVE_BACKPACK_BUTTON = "[data-test='remove-sauce-labs-backpack']"