import os
import pytest
import requests
from playwright.sync_api import sync_playwright
from utils.logger import get_logger

logger = get_logger()


def pytest_addoption(parser):
    parser.addoption("--app-base-url", action="store", default=os.getenv("BASE_URL", "https://example.com"))

    # Playwright options（加 pw- 前缀，避免跟别的插件撞名）
    parser.addoption("--pw-headless", action="store", default=os.getenv("PW_HEADLESS", "true"))
    parser.addoption("--pw-slowmo", action="store", default=os.getenv("PW_SLOWMO", "0"))
    parser.addoption("--pw-browser", action="store",default=os.getenv("PW_BROWSER", "chromium"))

@pytest.fixture(scope="session")
def base_url(request) -> str:
    return request.config.getoption("--app-base-url")


@pytest.fixture(scope="session")
def api() -> requests.Session:
    """
    API validation / workflow E2E 
    """
    s = requests.Session()
    token = os.getenv("API_TOKEN")
    if token:
        s.headers.update({"Authorization": f"Bearer {token}"})
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def browser(request):
    headless_raw = str(request.config.getoption("--pw-headless")).lower().strip()
    headless = headless_raw not in ("false", "0", "no")

    slowmo = int(request.config.getoption("--pw-slowmo"))
    browser_name = request.config.getoption("--pw-browser")

    with sync_playwright() as pw:
        btype = getattr(pw, browser_name)
        b = btype.launch(headless=headless, slow_mo=slowmo)
        yield b
        b.close()

@pytest.fixture()
def context(browser, base_url, request):
    """
    Function scope：every test create a new context，isolated the cookies/session。
    try to add：record_video_dir, timezone, locale etc.
    """
    ctx = browser.new_context(base_url=base_url)
    yield ctx

    # if failed then provide screenshot/trace 
    try:
        rep = getattr(request.node, "rep_call", None)
        if rep and rep.failed:
            logger.error(f"[FAIL] {request.node.nodeid}")
    finally:
        ctx.close()


@pytest.fixture()
def page(context, request):
    p = context.new_page()
    yield p
    p.close()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call): 
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
