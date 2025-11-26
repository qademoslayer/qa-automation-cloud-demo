# tests/practice/test_prac.py
import allure


@allure.title("Basic arithmetic sanity test")
def test_basic_math():
    with allure.step("Compute 2 + 2"):
        result = 2 + 2
    with allure.step("Verify result is 4"):
        assert result == 4
