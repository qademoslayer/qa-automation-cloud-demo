import os
import pytest
import allure
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import get_logger

logger = get_logger()


@pytest.fixture()
def driver():
    """Selenium WebDriver fixture (CI-friendly)."""
    options = Options()

    # local debug friendly
    options.add_argument("--start-maximized")

    # CI friendly headless
    if os.getenv("CI", "").lower() == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    drv = webdriver.Chrome(options=options)
    drv.set_page_load_timeout(30)

    yield drv

    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot + page source when Selenium test fails (audit evidence)."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            try:
                allure.attach(
                    drv.get_screenshot_as_png(),
                    name=f"failure_screenshot_{ts}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                logger.warning(f"Allure screenshot attach failed: {e}")

            try:
                allure.attach(
                    drv.page_source,
                    name=f"page_source_{ts}.html",
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception as e:
                logger.warning(f"Allure page source attach failed: {e}")

            try:
                allure.attach(
                    drv.current_url,
                    name="current_url",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception as e:
                logger.warning(f"Allure url attach failed: {e}")
