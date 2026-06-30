from playwright.sync_api import expect
from ultis.messages import ERROR_LOGIN_FAILED, ERROR_USERNAME_REQUIRED
from ultis.data_reader import get_user_from_json
import allure


@allure.feature("Login Feature")
@allure.link("https://www.saucedemo.com/", name="Login Page")
class TestLogin:

    @allure.story("Login with valid credentials")
    @allure.title("TC_LOGIN_001: Login thành công")
    def test_login_success(self, open_login_page):
        user = get_user_from_json("validUser")
        open_login_page.login(user["username"], user["password"])

        expect(open_login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(open_login_page.page.locator(".title")).to_have_text("Products")

    @allure.story("Login with invalid credentials")
    @allure.title("TC_LOGIN_002: Login sai password")
    def test_login_wrong_password(self, open_login_page):
        user = get_user_from_json("invalidPassword")
        open_login_page.login(user["username"], user["password"])

        expect(open_login_page.error_message()).to_be_visible()
        expect(open_login_page.error_message()).to_contain_text(ERROR_LOGIN_FAILED)

    @allure.story("Login with invalid credentials")
    @allure.title("TC_LOGIN_003: Login sai username")
    def test_login_wrong_username(self, open_login_page):
        user = get_user_from_json("invalidUsername")
        open_login_page.login(user["username"], user["password"])

        expect(open_login_page.error_message()).to_be_visible()
        expect(open_login_page.error_message()).to_contain_text(ERROR_LOGIN_FAILED)

    @allure.story("Login with empty credentials")
    @allure.title("TC_LOGIN_004: Login để trống dữ liệu")
    def test_login_empty_fields(self, open_login_page):
        user = get_user_from_json("emptyFields")
        open_login_page.login(user["username"], user["password"])

        expect(open_login_page.error_message()).to_be_visible()
        expect(open_login_page.error_message()).to_contain_text(ERROR_USERNAME_REQUIRED)
