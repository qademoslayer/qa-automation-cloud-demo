from __future__ import annotations
import re
from datetime import datetime

DATE_FMT = "%Y-%m-%d"

def assert_required(value, field_name: str):
    assert value is not None and str(value).strip() != "", f"{field_name} is required"

def assert_int_in_range(value, field_name: str, min_v: int, max_v: int):
    assert isinstance(value, int), f"{field_name} must be int"
    assert min_v <= value <= max_v, f"{field_name} must be between {min_v} and {max_v}"

def assert_decimal_format(value: str, field_name: str, max_dp: int = 2):
    # e.g. "12.34"
    pattern = rf"^\d+(\.\d{{1,{max_dp}}})?$"
    assert re.match(pattern, str(value)), f"{field_name} invalid decimal format"

def assert_date_ymd(value: str, field_name: str):
    try:
        datetime.strptime(value, DATE_FMT)
    except Exception:
        raise AssertionError(f"{field_name} must be YYYY-MM-DD")
