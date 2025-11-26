import re
import allure


# email validation
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# password validation
def is_valid_password(pwd: str) -> bool:
    return len(pwd) >= 6


# age validation
def is_valid_age(age: int) -> bool:
    return age >= 18


@allure.title("Validation - Email Should Be Valid")
def test_email_valid():
    with allure.step("Validate a correct email format"):
        assert is_valid_email("test@example.com") is True


@allure.title("Validation - Email Should Be Invalid")
def test_email_invalid():
    with allure.step("Validate incorrect email format"):
        assert is_valid_email("invalid-email") is False


@allure.title("Validation - Password Minimum Length")
def test_password_length():
    with allure.step("Validate password length >= 6"):
        assert is_valid_password("123456") is True
        assert is_valid_password("123") is False


@allure.title("Validation - Age must be >= 18")
def test_age_validation():
    with allure.step("Validate adult age"):
        assert is_valid_age(20) is True
        assert is_valid_age(15) is False
