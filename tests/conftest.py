import os
import pytest
import requests
import allure
from playwright.sync_api import sync_playwright, expect
from utils.logger import get_logger
from pathlib import Path

ARTIFACTS_DIR = Path("test-artifacts")
VIDEO_DIR = ARTIFACTS_DIR / "videos"
TRACE_DIR = ARTIFACTS_DIR / "traces"
STORAGE_STATE = Path(".auth") / "storage_state.json"

logger = get_logger()

#test
def _ensure_artifact_dirs():
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)

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
    Add: video + trace (attach to Allure on failure)
    """
    _ensure_artifact_dirs()

    ctx = browser.new_context(
        base_url=base_url,
        record_video_dir=str(VIDEO_DIR),
        record_video_size={"width": 1280, "height": 720},
    )

    # Start tracing for every test; only save on failure
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed

    try:
        if failed:
            logger.error(f"[FAIL] {request.node.nodeid}")

            trace_path = TRACE_DIR / f"{request.node.name}.zip"
            ctx.tracing.stop(path=str(trace_path))

            allure.attach.file(
                str(trace_path),
                name="playwright-trace",
                attachment_type=allure.attachment_type.ZIP
            )
        else:
            ctx.tracing.stop()
    except Exception as e:
        logger.warning(f"[TEARDOWN] trace attach failed: {e}")
    finally:
        ctx.close()

@pytest.fixture()
def page(context, request):
    p = context.new_page()
    yield p

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    video_path = None

    try:
        if failed:
            png = p.screenshot(full_page=True)
            allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)

            if p.video:
                video_path = p.video.path()
    except Exception as e:
        logger.warning(f"[TEARDOWN] screenshot/video capture failed: {e}")
    finally:
        p.close()

    # video file is finalized only after page.close()
    try:
        if failed and video_path and os.path.exists(video_path):
            allure.attach.file(
                video_path,
                name="video",
                attachment_type=allure.attachment_type.MP4
            )
    except Exception as e:
        logger.warning(f"[TEARDOWN] video attach failed: {e}")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call): 
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="session")
def ensure_storage_state(browser, base_url):
    """
    只要 storage_state.json 不存在，就执行一次登录并保存状态。
    """
    if STORAGE_STATE.exists():
        return str(STORAGE_STATE)

    STORAGE_STATE.parent.mkdir(parents=True, exist_ok=True)

    user = os.getenv("UI_USER", "demo")
    pwd = os.getenv("UI_PASS", "demo")

    ctx = browser.new_context(base_url=base_url)
    page = ctx.new_page()

    page.goto("/login", wait_until="domcontentloaded")
    page.locator('input[name="username"]').fill(user)
    page.locator('input[name="password"]').fill(pwd)
    page.locator('button[type="submit"]').click()

    # 验证登录成功（用稳定元素）
    expect(page.locator("h1")).to_have_text("Dashboard", timeout=15000)

    # 保存 cookie/localStorage/sessionStorage
    ctx.storage_state(path=str(STORAGE_STATE))

    page.close()
    ctx.close()

    return str(STORAGE_STATE)

@pytest.fixture()
def authed_context(browser, base_url, ensure_storage_state, request):
    _ensure_artifact_dirs()

    ctx = browser.new_context(
        base_url=base_url,
        storage_state=ensure_storage_state,
        record_video_dir=str(VIDEO_DIR),
        record_video_size={"width": 1280, "height": 720},
    )

    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed

    try:
        if failed:
            logger.error(f"[FAIL] {request.node.nodeid}")

            trace_path = TRACE_DIR / f"{request.node.name}.zip"
            ctx.tracing.stop(path=str(trace_path))

            allure.attach.file(
                str(trace_path),
                name="playwright-trace",
                attachment_type=allure.attachment_type.ZIP
            )
        else:
            ctx.tracing.stop()
    except Exception as e:
        logger.warning(f"[TEARDOWN] trace attach failed: {e}")
    finally:
        ctx.close()

@pytest.fixture()
def authed_page(authed_context, request):
    p = authed_context.new_page()
    yield p

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    video_path = None

    try:
        if failed:
            png = p.screenshot(full_page=True)
            allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)

            if p.video:
                video_path = p.video.path()
    except Exception as e:
        logger.warning(f"[TEARDOWN] screenshot/video capture failed: {e}")
    finally:
        p.close()

    try:
        if failed and video_path and os.path.exists(video_path):
            allure.attach.file(
                video_path,
                name="video",
                attachment_type=allure.attachment_type.MP4
            )
    except Exception as e:
        logger.warning(f"[TEARDOWN] video attach failed: {e}")



