import pytest
import dotenv
import allure
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from ultis.data_reader import get_user_from_json


_PROJECT_ROOT = Path(__file__).parent
_env_file = _PROJECT_ROOT / ".env"
if not _env_file.is_file():
    _env_file = _PROJECT_ROOT.parent / ".env"
dotenv.load_dotenv(_env_file)

@pytest.fixture(
    scope="function",
    params=["chromium", "firefox"],
    ids=["chromium", "firefox"],
)
def page(request):
    browser_type = request.param
    headless = False

    with sync_playwright() as p:
        if browser_type == "chromium":
            browser = p.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")

        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        yield page

        context.close()
        browser.close()

@pytest.fixture(scope="function")
def open_login_page(page):
    login_page = LoginPage(page)
    login_page.page.goto(os.getenv('BASE_URL'))
    yield login_page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        page = item.funcargs.get("page") or (
            item.funcargs.get("login").page if item.funcargs.get("login") else None
        )

        if page:
            status = "PASSED" if rep.passed else "FAILED"
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"{item.name}_{status}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                allure.attach(
                    body=f"Could not capture screenshot: {e}",
                    name=f"{item.name}_SCREENSHOT_ERROR",
                    attachment_type=allure.attachment_type.TEXT
                )


@pytest.fixture(scope="function")
def open_product_page(page):
    login_page = LoginPage(page)
    login_page.page.goto(os.getenv("BASE_URL"))
    #login_page.login(nếu ko dùng json mà nhập tay
    #    os.getenv("SAUCE_USERNAME"),
    #    os.getenv("SAUCE_PASSWORD"),
    #)
    user = get_user_from_json("validUser")
    login_page.login(user["username"], user["password"])
    product_page = ProductPage(page)
    yield product_page
