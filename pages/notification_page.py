from locators import NotificationPageLocators as nt_locators
from locators import TicketPageLocators as tk_locators
import allure

class NotificationPage:
    def __init__(self, page):
        self.page = page

    @allure.step("Get notification title")
    def title(self):
        return self.page.get_by_role("heading", name=nt_locators.TITLE)

    @allure.step("Get notification rows")
    def notification_rows(self):
        return self.page.locator(nt_locators.ROWS)

    @allure.step("Get ticket panel")
    def ticket_panel(self):
        return self.page.locator(tk_locators.PANEL)
