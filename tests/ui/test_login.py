from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_login_success(page):
    login = LoginPage(page)
    login.visit("https://the-internet.herokuapp.com/login")
    login.login("tomsmith", "SuperSecretPassword!")

   # Verify login success
    assert page.locator("div.flash.success").is_visible()
