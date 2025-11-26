import allure

def login(username: str, password: str) -> bool:
    return username == "admin" and password == "password123"


@allure.title("Simple Login Test - Correct username & password")
def test_login_success():
    with allure.step("Call login() with correct credentials"):
        result = login("admin", "password123")

    with allure.step("Verify login success"):
        assert result is True


@allure.title("Simple Login Test - Wrong password")
def test_login_wrong_password():
    with allure.step("Call login() with wrong password"):
        result = login("admin", "wrongpass")

    with allure.step("Verify login failure"):
        assert result is False


@allure.title("Simple Login Test - User not found")
def test_login_user_not_found():
    with allure.step("Call login() with unknown user"):
        result = login("unknown", "password123")

    with allure.step("Verify login failure for unknown user"):
        assert result is False
