from pages.base_page import BasePage

class LoginPage(BasePage):

    username_input = "#username"
    password_input = "#password"
    login_button = "button[type='submit']"

    def visit(self, url):
        self.page.goto(url)

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

