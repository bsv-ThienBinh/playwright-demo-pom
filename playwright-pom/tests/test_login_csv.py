import pytest
import allure
from playwright.sync_api import expect
from ultis.data_reader import get_users_from_csv
from ultis.messages import ERROR_LOGIN_FAILED, ERROR_USERNAME_REQUIRED


@allure.feature("Login Feature")
@allure.link("https://www.saucedemo.com/", name="Login Page")
class TestLoginCsv:

    @pytest.mark.parametrize("user", get_users_from_csv())
    @allure.title("TC_LOGIN_CSV: {user[test_case]}")
    def test_login_from_csv(self, open_login_page, user):
        open_login_page.login(user["username"], user["password"])

        if user["expected_result"] == "success":
            expect(open_login_page.page).to_have_url(
                "https://www.saucedemo.com/inventory.html"
            )
        elif user["expected_result"] == "login_failed":
            expect(open_login_page.error_message()).to_be_visible()
            expect(open_login_page.error_message()).to_contain_text(ERROR_LOGIN_FAILED)
        elif user["expected_result"] == "username_required":
            expect(open_login_page.error_message()).to_be_visible()
            expect(open_login_page.error_message()).to_contain_text(ERROR_USERNAME_REQUIRED)