from playwright.sync_api import expect
from ultis.messages import ERROR_LOGIN_FAILED
import allure

@allure.feature("Login Feature")
@allure.story("Login with invalid credentials")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="Login Page")
class TestLogin:
    @allure.title("GD02.8-04: Login sai")
    def test_gd02_8_04_login_with_invalid_credentials(self, open_login_page):
        open_login_page.login("admin", "wrongpass")
        expect(open_login_page.error_message()).to_be_visible()
        expect(open_login_page.error_message()).to_have_text(ERROR_LOGIN_FAILED)
        expect(open_login_page.page.locator("#main_section")).to_be_hidden()
