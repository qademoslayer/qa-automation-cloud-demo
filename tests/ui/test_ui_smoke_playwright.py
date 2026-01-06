import os
import pytest
from playwright.sync_api import expect

@pytest.mark.ui
def test_ui_smoke_login_and_dashboard(page):
    # demo credentials
    os.environ["UI_USER"] = "demo"
    os.environ["UI_PASS"] = "demo"

    # 1) 打开 login 页
    page.goto("/login", wait_until="domcontentloaded")

    # 2) 等输入框出现
    page.locator('input[name="username"]').wait_for(timeout=10000)
    page.locator('input[name="password"]').wait_for(timeout=10000)

    # 3) 输入帐号密码
    page.fill('input[name="username"]', os.getenv("UI_USER"))
    page.fill('input[name="password"]', os.getenv("UI_PASS"))

    # 4) 点击登录
    page.click('button[type="submit"]')

    # 5) 验证 Dashboard（不要用 URL，直接看页面内容）
    expect(page.locator("h1")).to_have_text("Dashboard", timeout=15000)
    expect(page.locator("#welcome")).to_contain_text("demo")
