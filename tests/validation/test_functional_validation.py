import pytest
from utils.validators import (
    assert_required,
    assert_int_in_range,
    assert_decimal_format,
    assert_date_ymd,
)

def test_required_fields_local_validation():
    payload = {"name": "Alice", "age": 30, "startDate": "2026-01-05", "amount": "12.50"}
    assert_required(payload.get("name"), "name")
    assert_required(payload.get("startDate"), "startDate")

def test_numeric_ranges_and_formats_local_validation():
    payload = {"age": 30, "amount": "12.50"}
    assert_int_in_range(payload["age"], "age", 18, 120)
    assert_decimal_format(payload["amount"], "amount", max_dp=2)

@pytest.mark.parametrize("bad_date", ["2026/01/05", "05-01-2026", "2026-13-01", ""])
def test_date_format_ymd_negative(bad_date):
    with pytest.raises(AssertionError):
        assert_date_ymd(bad_date, "startDate")

@pytest.mark.parametrize("bad_age", [-1, 0, 121, 999])
def test_age_out_of_range_negative(bad_age):
    with pytest.raises(AssertionError):
        assert_int_in_range(bad_age, "age", 18, 120)
