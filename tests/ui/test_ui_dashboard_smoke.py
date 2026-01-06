import pytest
from playwright.sync_api import expect

@pytest.mark.ui
def test_dashboard_smoke_authed(authed_page):
    authed_page.goto("/dashboard", wait_until="domcontentloaded")
    expect(authed_page.locator("h1")).to_have_text("Dashboard", timeout=10000)
