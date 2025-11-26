from pages.base_page import BasePage

class DashboardPage(BasePage):

    welcome_text = "#welcome"

    def get_welcome_message(self):
        return self.page.inner_text(self.welcome_text)
