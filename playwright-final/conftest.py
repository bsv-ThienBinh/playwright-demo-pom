import re
import pytest
import dotenv
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.ticket_page import TicketPage
import allure

_PROJECT_ROOT = Path(__file__).parent
_REPO_ROOT = _PROJECT_ROOT.parent
dotenv.load_dotenv(_PROJECT_ROOT / '.env')
dotenv.load_dotenv(_REPO_ROOT / '.env')


def _safe_name(name):
    return re.sub(r"[^\w.\-]+", "_", name).strip("_")

###NNTT: hook để chụp hình khi mà testcase xong để report được clear hơn. 
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    page = item.funcargs.get("page")
    status = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"

    if page is None or status not in ("PASSED", "FAILED"):
        return
    for state in ("load", "networkidle"):
        try:
            page.wait_for_load_state(state, timeout=3000)
        except Exception:
            pass

    try:
        png = page.screenshot(full_page=True)
    except Exception as exc:
        print(f"[screenshot] could not capture for {item.name}: {exc}")
        return

    allure.attach(
        png,
        name=f"{_safe_name(item.name)}_{status}",
        attachment_type=allure.attachment_type.PNG,
    )
    if status == "FAILED":
        try:
            allure.attach(page.url, name="Page URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(
                page.content(), name="Page HTML", attachment_type=allure.attachment_type.HTML
            )
        except Exception:
            pass




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