from pages.base_page import BasePage

class DashboardPage(BasePage):

    welcome_text = "#welcome"

    def get_welcome_message(self):
        self.page.wait_for_selector(self.welcome_text)
        return self.page.inner_text(self.welcome_text)
