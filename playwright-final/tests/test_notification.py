from playwright.sync_api import expect
from pages.notification_page import NotificationPage
import allure

@allure.feature("Notification Feature")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="Notification Page")
class TestNotification:
    @allure.title("GD01_004: Navigation")
    def test_gd01_004_open_notification_tab(self, open_ticket_page):
        open_ticket_page.open_notification_tab()
        notification_page = NotificationPage(open_ticket_page.page)
        expect(notification_page.title()).to_be_visible()
        expect(notification_page.notification_rows()).to_have_count(3)
        expect(notification_page.ticket_panel()).to_be_hidden()
