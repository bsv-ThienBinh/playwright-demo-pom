import pytest
import dotenv
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.ticket_page import TicketPage
import allure
_PROJECT_ROOT = Path(__file__).parent
dotenv.load_dotenv(_PROJECT_ROOT / '.env')




@pytest.fixture(scope="function")
def page():
    headless = False
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        yield page

        context.close()
        browser.close()


@pytest.fixture(scope="function")
def open_login_page(page):
    login_page = LoginPage(page)
    login_page.page.goto(os.getenv('BASE_URL'))
    yield login_page

@pytest.fixture(scope="function")
def open_ticket_page(page):
    login_page = LoginPage(page)
    login_page.page.goto(os.getenv('BASE_URL'))
    login_page.login(os.getenv('LOGIN_ID'), os.getenv('LOGIN_PASSWORD'))
    ticket_page = TicketPage(page)
    yield ticket_page