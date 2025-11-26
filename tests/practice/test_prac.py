import allure
import pytest

@allure.epic("Random Tests")
@allure.feature("Contract Validation")
@allure.story("Basic schema validation")
def test_re_duplicate():
    s = "paypalpython"
    seen = set()
    result = []
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    assert ''.join(result) == "paylthon"


def test_find_missing():
    nums = [0, 1, 2, 4, 5]
    n = len(nums)
    total = n * (n + 1) // 2
    assert total - sum(nums) == 3


def test_val_response():
    response = {"id":1, "name":"user", "email":"x@x.com"}
    expected = ["id", "name", "email"]
    missing = [f for f in expected if f not in response]
    assert missing == []


def test_compare_data():
    api = {"user":"cheng", "status":"active", "balance":100}
    db  = {"user":"cheng", "status":"Inactive", "balance":100}
    mismatched = [(k, api[k], db.get(k)) for k in api if api[k] != db.get(k)]
    assert mismatched == [("status", "active", "Inactive")]


def test_validate_schema():
    api_data = {"id":1, "name":"user", "email":"u@x.com", "role":"admin"}
    schema = ["id", "name", "email"]
    missing = [k for k in schema if k not in api_data]
    extra   = [k for k in api_data if k not in schema]
    assert missing == []
    assert extra == ["role"]


def test_count_occurrences():
    items = ['apple','banana','apple','orange','banana','apple']
    counts = {}
    for i in items:
        counts[i] = counts.get(i, 0) + 1
    assert counts == {"apple":3, "banana":2, "orange":1}
