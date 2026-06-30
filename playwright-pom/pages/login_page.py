from locators import LoginPageLocators as lg_locators
import allure
class LoginPage: 
    def __init__(self, page):
        self.page = page

    @allure.step("Input username: {username}")
    def input_username(self, username):
        self.page.fill(lg_locators.INPUT_USERNAME, username)

    @allure.step("Input password: {password}")    
    def input_password(self, password):
        self.page.fill(lg_locators.INPUT_PASSWORD, password)

    @allure.step("Click login button")
    def click_login_button(self):
        self.page.click(lg_locators.BUTTON_LOGIN)

    @allure.step("Login with username: {username} and password: {password}")
    def login(self, username, password):
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()
            
    @allure.step("Get error message element")   
    def error_message(self):
        return self.page.locator(lg_locators.ERROR_MESSAGE)

