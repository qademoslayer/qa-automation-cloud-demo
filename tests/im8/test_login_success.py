from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_im8_user_can_login_successfully(page):
    """
    Verify that a valid IM8 user can login successully
    and see the dashboard welcome message
    """

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.visit("https://im8.example.com/login")
    
    login_page.login("valid_user", "valid_password")

    welcome_text = dashboard_page.get_welcome_message()

    assert "welcome" in welcome_text